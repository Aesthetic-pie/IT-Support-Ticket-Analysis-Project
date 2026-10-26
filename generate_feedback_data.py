import numpy as np
import pandas as pd

rng = np.random.default_rng(42)


# SETTINGS

N_EMPLOYEES = 60
FEEDBACK_PER_EMPLOYEE = 25
LABEL_NOISE = 0.06      # share of comments whose overall label is flipped to a neighbour class
THEMES = ["communication", "speed", "technical"]

first_names = ["Aiden", "Zoe", "Thabo", "Priya", "Liam", "Naledi", "Omar", "Chloe", "Sipho", "Mei",
               "Jabu", "Hannah", "Ravi", "Lerato", "Ethan", "Amara", "Kabelo", "Sofia", "Dev", "Nomsa"]


# PHRASE BANK: one pool of sentences per theme and polarity {n} = employee first name

bank = {
    "communication": {
        "strong": [
            "{n} explains technical problems in a way customers actually understand.",
            "Customers often mention how clear and friendly {n} is on calls.",
            "{n} keeps clients updated without being asked.",
            "Written replies from {n} are clear, polite and to the point.",
            "{n} is great at staying calm and reassuring upset customers.",
            "Handovers from {n} are always well documented, the team never has to chase for details.",
            "{n} listens well and asks the right questions before jumping in.",
            "Strong communicator, both with customers and inside the team.",
        ],
        "okay": [
            "{n}'s communication is fine, nothing special but no complaints either.",
            "{n} updates customers when needed, though it can be a bit basic.",
            "Tone with customers is acceptable, sometimes a little formal.",
            "{n} communicates adequately but rarely goes beyond the minimum.",
            "Replies from {n} are generally clear, occasionally too short.",
            "No real issues with how {n} talks to customers.",
        ],
        "weak": [
            "{n} struggles to explain solutions without too much jargon.",
            "Customers have complained that they never hear back from {n}.",
            "{n} comes across as short or impatient on calls.",
            "Ticket notes from {n} are vague, so colleagues often have to ask what was done.",
            "{n} does not keep clients updated and they end up chasing.",
            "Replies from {n} are sometimes unclear and cause back-and-forth.",
            "{n} avoids difficult conversations with customers.",
            "Communication is the main weakness, especially in written replies.",
        ],
    },
    "speed": {
        "strong": [
            "{n} clears tickets quickly and rarely misses a deadline.",
            "Response times from {n} are consistently among the best on the team.",
            "{n} handles a high volume without the quality dropping.",
            "{n} picks up urgent tickets straight away and gets them closed fast.",
            "Turnaround on {n}'s tickets is impressive.",
            "{n} manages time well and the backlog stays small.",
            "Very efficient, {n} is almost never close to breaching an SLA.",
        ],
        "okay": [
            "{n} works at a steady pace, meets most deadlines.",
            "Resolution times for {n} are about average for the team.",
            "{n} is reasonably quick but can slow down when the queue is busy.",
            "Speed is acceptable, a couple of tickets ran close to their SLA.",
            "{n} gets through a normal workload without trouble.",
            "Pace is okay, not the fastest but dependable.",
        ],
        "weak": [
            "{n} takes too long on routine tickets.",
            "Several of {n}'s tickets this month breached their SLA.",
            "{n} lets tickets sit in the queue before picking them up.",
            "Response times are slow and customers have noticed.",
            "{n} gets stuck on small details and the backlog keeps growing.",
            "{n} struggles to prioritise urgent tickets over simple ones.",
            "Speed is a concern, tickets take noticeably longer than for peers.",
        ],
    },
    "technical": {
        "strong": [
            "{n} diagnoses complex issues accurately, often on the first attempt.",
            "{n} is the person colleagues go to for tricky network and security problems.",
            "Solutions from {n} fix the root cause so tickets rarely come back.",
            "{n} has a deep understanding of our systems and keeps learning.",
            "Technical knowledge is excellent, {n} documents fixes in the knowledge base too.",
            "{n} troubleshoots methodically and finds problems others miss.",
            "Very few of {n}'s tickets get reopened.",
        ],
        "okay": [
            "{n} handles standard technical issues well enough.",
            "Technical skills are solid on common problems, still learning the harder ones.",
            "{n} follows the troubleshooting guides correctly.",
            "Knowledge is adequate for the role, {n} escalates when appropriate.",
            "{n} gets most routine fixes right.",
            "Technically fine for the level, some room to grow.",
        ],
        "weak": [
            "{n} often misdiagnoses the issue and tickets get reopened.",
            "{n} lacks confidence with more advanced technical problems.",
            "Too many of {n}'s fixes only treat the symptom, not the cause.",
            "{n} escalates issues that should be handled at their level.",
            "{n} needs more training on our core systems.",
            "Mistakes in troubleshooting steps cost the customer extra time.",
            "Technical gaps are visible, especially with security and account issues.",
        ],
    },
}

# comments that don't mention any theme, they only give a general impression or an example structure on how should the comments look like when testing the comments
generic = {
    "strong": ["Great quarter overall.", "A pleasure to have on the team.", "Consistently exceeds expectations.",
               "Keep it up, excellent work.", "Strong performer, could be a mentor soon."],
    "okay": ["Meets expectations overall.", "A decent quarter.", "Does the job.", "Steady, no big surprises.",
             "Average results this period."],
    "weak": ["Needs to step up.", "Performance is below expectations right now.", "Not where we need them to be yet.",
             "A difficult quarter overall.", "Needs close support and coaching."],
}

connectors_same = [" ", " Also, ", " On top of that, ", " Additionally, "]
connectors_contrast = [" However, ", " But ", " On the other hand, ", " That said, "]


# EMPLOYEES (hidden "true" skills, used to build the data and to check the results later)

employees = []
for i in range(N_EMPLOYEES):
    overall = rng.normal(0, 1)
    row = {"employee_id": f"EMP_{i+1:03d}", "first_name": first_names[i % len(first_names)]}
    for t in THEMES:
        row[f"true_{t}"] = overall * 0.8 + rng.normal(0, 0.7)
    employees.append(row)
emp_df = pd.DataFrame(employees)

supervisors = {"SUP_1": "formal", "SUP_2": "casual", "SUP_3": "terse"}


def to_polarity(skill):
    """Skill + noise -> strong / okay / weak for one comment."""
    x = skill + rng.normal(0, 0.8)
    if x > 0.5:
        return "strong"
    if x < -0.5:
        return "weak"
    return "okay"


score_map = {"strong": 1, "okay": 0, "weak": -1}


def apply_style(text, style):
    if style == "casual":
        text = text.lower().replace(". ", ", ").rstrip(".")
    elif style == "terse":
        text = text.replace(" However, ", "; ").replace(" But ", "; ")
        sentences = [s.strip() for s in text.split(".") if s.strip()]
        text = ". ".join(sentences[:2]) + "."
    return text



# GENERATE FEEDBACK

rows = []
for _, e in emp_df.iterrows():
    for k in range(FEEDBACK_PER_EMPLOYEE):
        sup = rng.choice(list(supervisors))
        n_themes = rng.choice([0, 1, 2, 3], p=[0.10, 0.35, 0.40, 0.15])
        chosen = list(rng.choice(THEMES, size=n_themes, replace=False)) if n_themes else []

        polarities = {t: "not_mentioned" for t in THEMES}
        parts, scores = [], []
        prev = None
        for t in chosen:
            pol = to_polarity(e[f"true_{t}"])
            polarities[t] = pol
            sentence = rng.choice(bank[t][pol]).format(n=e["first_name"])
            if prev is None:
                parts.append(sentence)
            else:
                contrast = (score_map[pol] * score_map[prev]) < 0
                conn = rng.choice(connectors_contrast if contrast else connectors_same)
                body = sentence if sentence.startswith(e["first_name"]) else sentence[0].lower() + sentence[1:]
                parts.append((conn.strip() + " " + body) if conn.strip() else sentence)
            prev = pol
            scores.append(score_map[pol])

        # general impression sentence (sometimes), also based on the employee's overall level
        if n_themes == 0 or rng.random() < 0.35:
            overall_skill = np.mean([e[f"true_{t}"] for t in THEMES])
            g = to_polarity(overall_skill)
            parts.append(rng.choice(generic[g]))
            scores.append(score_map[g])

        text = " ".join(parts)
        text = apply_style(text, supervisors[sup])

        # overall level from the average of what the comment says, plus noise
        s = np.mean(scores) + rng.normal(0, 0.25)
        level = "strong" if s > 0.4 else ("needs_coaching" if s < -0.4 else "average")

        # label noise: sometimes supervisors rate a bit differently than the words suggest
        if rng.random() < LABEL_NOISE:
            order = ["needs_coaching", "average", "strong"]
            idx = order.index(level)
            idx = min(2, max(0, idx + rng.choice([-1, 1])))
            level = order[idx]

        rows.append({
            "employee_id": e["employee_id"],
            "supervisor_id": sup,
            "date": pd.Timestamp("2024-01-01") + pd.Timedelta(days=int(rng.integers(0, 700))),
            "feedback_text": text,
            "performance_level": level,
            "communication": polarities["communication"],
            "speed": polarities["speed"],
            "technical": polarities["technical"],
        })

df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)
df.insert(0, "feedback_id", [f"FB_{i+1:05d}" for i in range(len(df))])
df["date"] = df["date"].dt.date

df.to_csv("synthetic_employee_feedback.csv", index=False)
emp_df.to_csv("employees_hidden_truth.csv", index=False)

print("Rows:", len(df))
print("\nOverall level:\n", df["performance_level"].value_counts(normalize=True).round(3))
print("\nDuplicate feedback texts:", df["feedback_text"].duplicated().sum())
print("\nExample comments:")
for t in df["feedback_text"].head(5):
    print(" -", t)
