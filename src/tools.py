"""Tools the agent can call.

There is one tool: run_lasso. It fits a Lasso regression on a CSV file
and returns the results as a plain dictionary (so it can be sent as JSON).
"""

import json
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LassoCV
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def run_lasso(csv_path, target, random_state=42):
    """Fit Lasso on a CSV file and report how well it predicts `target`.

    Steps:
    1. Load the data and check it is usable.
    2. Split it into a training set (80%) and a test set (20%).
    3. On the training set only: standardize the variables and fit Lasso,
       choosing the penalty strength (alpha) by 5-fold cross-validation.
    4. Measure R² on the test set, which the model never saw.
    """
    # --- 1. Load and check the data ---
    df = pd.read_csv(csv_path)

    if target not in df.columns:
        raise ValueError(
            f"Column '{target}' is not in {csv_path}. "
            f"Available columns: {', '.join(df.columns)}"
        )

    non_numeric = [c for c in df.columns if not pd.api.types.is_numeric_dtype(df[c])]
    if non_numeric:
        raise ValueError(
            f"These columns are not numeric: {', '.join(non_numeric)}. "
            "Lasso needs numbers only, so please convert or remove them first."
        )

    with_missing = [c for c in df.columns if df[c].isna().any()]
    if with_missing:
        raise ValueError(
            f"These columns have missing values: {', '.join(with_missing)}. "
            "Please fill or remove them first."
        )

    X = df.drop(columns=[target])  # the predictors: every other column
    y = df[target]                 # the outcome we want to predict

    # --- 2. Split into train and test sets ---
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state
    )

    # --- 3. Standardize, then fit Lasso with alpha chosen by cross-validation ---
    # Standardizing puts every variable on the same scale (mean 0, sd 1),
    # so the penalty treats them all equally.
    # LassoCV tries many alphas and keeps the one with the best
    # cross-validated prediction error on the training data.
    model = make_pipeline(StandardScaler(), LassoCV(cv=5))
    model.fit(X_train, y_train)
    lasso = model[-1]  # the fitted LassoCV step inside the pipeline

    # --- 4. Measure performance on the held-out test set ---
    test_r2 = r2_score(y_test, model.predict(X_test))

    # Split variables into kept (nonzero coefficient) and dropped (exactly zero).
    # Coefficients are "change in the outcome per 1 standard deviation of x".
    kept = {}
    dropped = []
    for name, coef in zip(X.columns, lasso.coef_):
        if coef == 0:
            dropped.append(name)
        else:
            kept[name] = round(float(coef), 3)

    # Sort kept variables from largest to smallest coefficient (in absolute value)
    kept = dict(sorted(kept.items(), key=lambda item: abs(item[1]), reverse=True))

    return {
        "target": target,
        "n_train": len(X_train),
        "n_test": len(X_test),
        "test_r2": round(float(test_r2), 4),
        "chosen_alpha": round(float(lasso.alpha_), 4),
        "kept_variables": kept,
        "dropped_variables": dropped,
    }


# Run this file directly to try the tool on the startup data:
#   .venv/bin/python src/tools.py
if __name__ == "__main__":
    data_path = Path(__file__).resolve().parent.parent / "data" / "startups.csv"
    result = run_lasso(str(data_path), "next_round_valuation_musd")
    print(json.dumps(result, indent=2))
