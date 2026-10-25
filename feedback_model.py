import re
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
from sklearn.model_selection import GroupShuffleSplit, GroupKFold, cross_val_predict
from sklearn.pipeline import Pipeline


# 1. Importing the two datasets

df = pd.read_csv("synthetic_employee_feedback.csv")
truth = pd.read_csv("employees_hidden_truth.csv")   # only used at the very end to CHECK my results

print("Rows:", len(df))
print(df["performance_level"].value_counts(normalize=True).round(3))


# 2. Cleaning the text

# Names are replaced with [NAME], otherwise the model could just learn "Kabelo = good" instead of learning what the feedback actually says about Kabelo's performance
names = truth["first_name"].unique().tolist()
name_pattern = re.compile(r"\b(" + "|".join(names) + r")(?:'s)?\b", flags=re.IGNORECASE)

def clean_text(text):
    return name_pattern.sub("NAME", text)

df["clean_text"] = df["feedback_text"].apply(clean_text)

# Exact duplicate comments (e.g. "[NAME] listens well and asks the right questions.") would end up in BOTH the train and test sets, which makes the score look better than it is
before = len(df)
df = df.drop_duplicates(subset="clean_text").reset_index(drop=True)
print(f"\nRemoved {before - len(df)} duplicate comments, {len(df)} left")


# 3. Defining the features (X) and targets (y)

X = df["clean_text"]
y = df["performance_level"]
groups = df["employee_id"]


# 4. Train/test split BY EMPLOYEE

# All comments about one employee stay together, so the model is always tested on employees it has never seen, like different employees
splitter = GroupShuffleSplit(n_splits=1, test_size=0.3, random_state=42)
train_idx, test_idx = next(splitter.split(X, y, groups))

X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

print("\nTraining comments:", len(X_train), "| Testing comments:", len(X_test))
print("Employees in both train and test:",
      len(set(groups.iloc[train_idx]) & set(groups.iloc[test_idx])), "(should be 0)")


# 5. Model 1: overall performance level (strong / average / needs_coaching)

def make_model():
    return Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)),
        ("classifier", LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)),
    ])

level_model = make_model()
level_model.fit(X_train, y_train)
y_pred = level_model.predict(X_test)

# A "dumb" model for comparison, mine has to beat this
dummy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
print("\nDummy accuracy:", round(accuracy_score(y_test, dummy.predict(X_test)), 3))

print("Model accuracy:", round(accuracy_score(y_test, y_pred), 3))
print("Model macro F1:", round(f1_score(y_test, y_pred, average="macro"), 3))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

labels = ["needs_coaching", "average", "strong"]
print("Confusion Matrix (rows = actual, columns = predicted):")
print(pd.DataFrame(confusion_matrix(y_test, y_pred, labels=labels), index=labels, columns=labels))


# 6. Models 2-4: which themes are mentioned, and are they a strength or a weakness?

themes = ["communication", "speed", "technical"]
theme_models = {}

for theme in themes:
    m = make_model()
    m.fit(X_train, df[theme].iloc[train_idx])
    pred = m.predict(X_test)
    theme_models[theme] = m
    print(f"\n{theme.upper()} model, accuracy: {accuracy_score(df[theme].iloc[test_idx], pred):.3f}, "
          f"macro F1: {f1_score(df[theme].iloc[test_idx], pred, average='macro'):.3f}")


# 7. What does the model rely on? (a quick sanity check)

tfidf = level_model.named_steps["tfidf"]
clf = level_model.named_steps["classifier"]
words = np.array(tfidf.get_feature_names_out())

print("\nWords pushing towards each level:")
for i, cls in enumerate(clf.classes_):
    top = words[np.argsort(clf.coef_[i])[-6:][::-1]]
    print(f"  {cls}: {', '.join(top)}")


# 8. Predictions for EVERY comment without cheating

# Each comment is predicted by a model that never saw that employee (5 folds, split by employee), so the employee profiles below are fair
cv = GroupKFold(n_splits=5)
df["pred_level"] = cross_val_predict(make_model(), X, y, cv=cv, groups=groups)
for theme in themes:
    df[f"pred_{theme}"] = cross_val_predict(make_model(), X, df[theme], cv=cv, groups=groups)


# 9. Building a profile for each employee

score_map = {"strong": 1, "okay": 0, "weak": -1}

profiles = []
for emp, g in df.groupby("employee_id"):
    row = {
        "employee_id": emp,
        "n_comments": len(g),
        "pct_strong": (g["pred_level"] == "strong").mean(),
        "pct_needs_coaching": (g["pred_level"] == "needs_coaching").mean(),
    }
    row["performance_score"] = row["pct_strong"] - row["pct_needs_coaching"]
    for theme in themes:
        mentioned = g[g[f"pred_{theme}"] != "not_mentioned"][f"pred_{theme}"]
        # need at least 3 mentions, otherwise the average isn't reliable
        row[f"{theme}_score"] = mentioned.map(score_map).mean() if len(mentioned) >= 3 else np.nan
    profiles.append(row)

profiles = pd.DataFrame(profiles).set_index("employee_id")

# bottom 20% = needs coaching, top 20% = top performers
low_cut = profiles["performance_score"].quantile(0.20)
high_cut = profiles["performance_score"].quantile(0.80)
profiles["group"] = np.where(profiles["performance_score"] <= low_cut, "needs_coaching",
                     np.where(profiles["performance_score"] >= high_cut, "top_performer", "middle"))

print("\nEmployee groups:\n", profiles["group"].value_counts())


# 10. Recommending mentors: top performers who are strong where the struggling employee is weak, so that the mentors can help them by coaching them

MAX_MENTEES = 2
mentees_count = {}
recommendations = []

top_performers = profiles[profiles["group"] == "top_performer"]

for emp, row in profiles[profiles["group"] == "needs_coaching"].iterrows():
    theme_scores = row[[f"{t}_score" for t in themes]].dropna()
    if theme_scores.empty:
        continue
    weakest = theme_scores.idxmin().replace("_score", "")

    # top performers sorted by how strong they are in that theme
    candidates = top_performers[f"{weakest}_score"].dropna().sort_values(ascending=False)
    mentor = None
    for cand in candidates.index:
        if mentees_count.get(cand, 0) < MAX_MENTEES:
            mentor = cand
            break
    if mentor is None:
        continue

    mentees_count[mentor] = mentees_count.get(mentor, 0) + 1
    recommendations.append({
        "employee_to_coach": emp,
        "weakest_area": weakest,
        "their_score": round(row[f"{weakest}_score"], 2),
        "recommended_mentor": mentor,
        "mentor_score_in_area": round(top_performers.loc[mentor, f"{weakest}_score"], 2),
    })

recommendations = pd.DataFrame(recommendations)
print("\nMentor recommendations:\n", recommendations.to_string(index=False))

profiles.round(2).to_csv("employee_profiles.csv")
recommendations.to_csv("mentor_recommendations.csv", index=False)


# 11. Checking my results against the hidden truth (only possible because the data is synthetic)

truth = truth.set_index("employee_id")
truth["true_overall"] = truth[[f"true_{t}" for t in themes]].mean(axis=1)
check = profiles.join(truth)

corr = check["performance_score"].corr(check["true_overall"], method="spearman")
print("\nCorrelation between my performance score and the true skill:", round(corr, 3))

true_bottom = set(truth["true_overall"].nsmallest(len(profiles[profiles["group"] == "needs_coaching"])).index)
flagged = set(profiles[profiles["group"] == "needs_coaching"].index)
print("Flagged as needs coaching who are truly in the weakest group:",
      f"{len(flagged & true_bottom)} out of {len(flagged)}")

if len(recommendations):
    good = 0
    for _, r in recommendations.iterrows():
        mentor_skill = truth.loc[r["recommended_mentor"], f"true_{r['weakest_area']}"]
        mentee_skill = truth.loc[r["employee_to_coach"], f"true_{r['weakest_area']}"]
        good += mentor_skill > mentee_skill
    print(f"Mentors who are truly better than the mentee in that area: {good} out of {len(recommendations)}")

# 12. Testing the model on feedback I type myself

def analyse_feedback(text):
    text = clean_text(text)
    probs = level_model.predict_proba([text])[0]
    print(f'\nFeedback: "{text}"')
    print("  Overall:", level_model.predict([text])[0],
          "| chances:", {c: round(float(pr), 2) for c, pr in zip(level_model.classes_, probs)})
    for theme in themes:
        print(f"  {theme}:", theme_models[theme].predict([text])[0])

analyse_feedback("Sipho explains issues clearly to customers but takes too long to close tickets.")
analyse_feedback("Priya is excellent technically and a great mentor for the team.")
analyse_feedback("Needs close support, customers complained and several tickets breached SLA.")
analyse_feedback("Meets expectations.")
analyse_feedback("Natasha explains issues in the simplest terms to customers and close tickets more quickly")
