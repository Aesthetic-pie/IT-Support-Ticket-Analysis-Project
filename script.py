"""SLA breach prediction for IT support tickets.

Converted from Script.ipynb. Place synthetic_it_support_tickets.csv in the
same folder as this script (or pass a different path as the first argument).
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def main():
    # Importing the dataset
    csv_path = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else Path(__file__).resolve().parent / "synthetic_it_support_tickets.csv"
    )
    df = pd.read_csv(csv_path)
    print(df.head())
    print(df.tail())

    # Quick exploration
    print(df["sla_plan"].value_counts())
    print(df["region"].value_counts())
    print(df["status"].value_counts())
    print(df["resolution_time_hours"].max())
    print(df["resolution_time_hours"].min())
    print(df["resolution_time_hours"].mode())
    print(df["has_attachment"].value_counts())
    print(df["resolution_time_hours"].mean())
    print(df["reopened"].value_counts())
    df.info()

    # Filling in the missing values and removing unnecessary features [data cleaning & preprocessing]
    df = df.drop(columns=[
        "region",
        "resolution_summary",
        # identifiers and text, not useful for predicting
        "ticket_id",
        "customer_id",
        "created_at",
        "initial_message",
        "agent_first_reply",
        # only known AFTER the ticket is handled, so the model can't use them in real life
        "customer_sentiment",
        "csat_score",
    ])

    # Checking the missing values
    # resolution_time_hours is only missing for tickets that aren't finished yet
    # (open, in_progress, on_hold), so it is not filled with random numbers;
    # only finished tickets are used later on
    print(df.isnull().sum())
    print(df["issue_type"].value_counts())

    df = pd.get_dummies(
        df,
        columns=["issue_type", "priority", "status"],
        dtype=int,
    )

    sla_plan = {
        "platinum": 1,
        "gold": 2,
        "standard": 3,
    }
    df["sla_plan"] = df["sla_plan"].map(sla_plan)

    df.info()
    print(df.head())
    print(df["status_resolved"].value_counts())

    # Defining the new column before setting it as a target
    # Only resolved tickets can be judged as breached or not
    resolved = df[df["status_resolved"] == 1].copy()

    # sla_plan was mapped earlier: platinum = 1, gold = 2, standard = 3
    # these hours are example values since we are dealing with synthetic data
    sla_hours = {1: 8, 2: 16, 3: 24}

    # breach = the ticket took longer than its plan allows
    resolved["sla_breach"] = (
        resolved["resolution_time_hours"] > resolved["sla_plan"].map(sla_hours)
    ).astype(int)

    print(resolved["sla_breach"].value_counts(normalize=True))

    # Defining the features as well as the target
    # Left out on purpose: resolution_time_hours (used to make the target),
    # reopened and status (only known after the ticket is handled)
    X = resolved[[
        "customer_segment",
        "channel",
        "product_area",
        "platform",
        "issue_type_account_access",
        "issue_type_billing_problem",
        "issue_type_bug",
        "issue_type_feature_request",
        "issue_type_how_to",
        "issue_type_other",
        "issue_type_performance",
        "issue_type_security_concern",
        "priority_high",
        "priority_low",
        "priority_medium",
        "priority_urgent",
        "sla_plan",
        "has_attachment",
    ]]

    y = resolved["sla_breach"]

    # Conducting a train_test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.3,
        random_state=42,
        stratify=y,
    )

    # Checking the train/test split
    print("Training features:", X_train.shape)
    print("Testing features:", X_test.shape)
    print("Training target:", y_train.shape)
    print("Testing target:", y_test.shape)

    # Training the model
    categorical_cols = X_train.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    numerical_cols = X_train.select_dtypes(include=["number"]).columns.tolist()

    numerical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ])

    preprocessor = ColumnTransformer([
        ("num", numerical_pipeline, numerical_cols),
        ("cat", categorical_pipeline, categorical_cols),
    ])

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(
            class_weight="balanced",
            max_iter=1000,
            random_state=42,
        )),
    ])

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Evaluation
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Precision:", precision_score(y_test, y_pred, zero_division=0))
    print("Recall:", recall_score(y_test, y_pred, zero_division=0))
    print("F1-score:", f1_score(y_test, y_pred, zero_division=0))

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # Comparing against a "dumb" model that always guesses the most common answer
    # my model has to beat this, otherwise it hasn't learned anything
    dummy = DummyClassifier(strategy="most_frequent")
    dummy.fit(X_train, y_train)
    dummy_pred = dummy.predict(X_test)

    print("Dummy accuracy:", accuracy_score(y_test, dummy_pred))
    print("Dummy recall:", recall_score(y_test, dummy_pred, zero_division=0))
    print("Model accuracy:", accuracy_score(y_test, y_pred))
    print("Model recall:", recall_score(y_test, y_pred, zero_division=0))

    # Testing the model on 5 different splits of the data to see if the score is stable
    scores = cross_val_score(model, X, y, cv=5, scoring="roc_auc")
    print("ROC-AUC for each split:", scores.round(3))
    print("Average:", scores.mean().round(3))

    # Checking which features the model relies on most (the leakage check)
    # if one feature controls everything, something is still leaking
    feature_names = model.named_steps["preprocessor"].get_feature_names_out()
    coefficients = model.named_steps["classifier"].coef_[0]

    importance = pd.Series(coefficients, index=feature_names).sort_values(
        key=abs, ascending=False
    )
    print(importance.head(10))

    # Testing the model on a brand new ticket made up by hand
    # the columns must match that of X exactly
    new_ticket = pd.DataFrame([{
        "customer_segment": "enterprise",
        "channel": "email",
        "product_area": "billing",
        "platform": "web",
        "issue_type_account_access": 0,
        "issue_type_billing_problem": 1,
        "issue_type_bug": 0,
        "issue_type_feature_request": 0,
        "issue_type_how_to": 0,
        "issue_type_other": 0,
        "issue_type_performance": 0,
        "issue_type_security_concern": 0,
        "priority_high": 0,
        "priority_low": 1,
        "priority_medium": 0,
        "priority_urgent": 0,
        "sla_plan": 1,  # 1 = platinum, 2 = gold, 3 = standard
        "has_attachment": 0,
    }])

    print("Predicted class (1 = breach):", model.predict(new_ticket)[0])
    print("Chance of breach:", model.predict_proba(new_ticket)[0][1].round(3))

    # Testing the model on real tickets from the test set, side by side with the truth
    y_proba = model.predict_proba(X_test)[:, 1]

    results = X_test.copy()
    results["actual_sla_breach"] = y_test
    results["predicted_sla_breach"] = y_pred
    results["chance_of_sla_breach"] = y_proba.round(3)

    print(results[[
        "sla_plan",
        "priority_low",
        "priority_urgent",
        "actual_sla_breach",
        "predicted_sla_breach",
        "chance_of_sla_breach",
    ]].head(10))


if __name__ == "__main__":
    main()
