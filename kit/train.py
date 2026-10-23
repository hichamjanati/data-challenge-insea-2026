"""Baseline: a linear discriminant analysis (LDA) with default settings on the table columns,
trained on the complete rows only.

Usage: uv run python -m kit.train
Writes submissions/baseline.csv. Reported score: 5-fold cross-validated log loss on the training rows used.

This is a starting point, not a recommendation. Two of its choices are worth questioning on day one:
  - it drops every training ad with a missing value in the columns it uses;
  - at prediction time, a test ad with a missing value gets the train sale rate, since the model never saw such ads.
"""
from datetime import date
import numpy as np, pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from kit.data import SUBMISSIONS, TARGET, load_train, load_test

NUMERIC = ["reg_year", "km", "engine_l", "price_mad", "seats", "doors", "post_month"]
CATEGORICAL = ["make", "model", "gearbox", "fuel", "body_type", "color", "city", "seller_type"]
# we use only some of the features to speed up the training

train, test = load_train(), load_test()
base_rate = train[TARGET].mean()
cols = NUMERIC + CATEGORICAL
complete = train[cols].notna().all(axis=1)
print(f"train: {len(train):,} ads, {complete.sum():,} complete on the {len(cols)} columns used ({complete.mean():.1%})")
X, y = train.loc[complete, cols], train.loc[complete, TARGET]

# numeric columns as they are, categorical columns one-hot encoded, then LDA: no scaling, no tuning
model = Pipeline([
    ("prep", ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL)],
                               remainder="passthrough")),
    ("clf", LinearDiscriminantAnalysis()),
])
cv = -cross_val_score(model, X, y, cv=5, scoring="neg_log_loss")
print(f"5-fold log loss on the complete training rows: {cv.mean():.4f} (+/- {cv.std():.4f})")
model.fit(X, y)

test_complete = test[cols].notna().all(axis=1)
p = np.full(len(test), base_rate)
p[test_complete.values] = model.predict_proba(test.loc[test_complete, cols])[:, 1]
p = np.clip(p, 0.01, 0.99)
print(f"test: {len(test):,} ads, {(~test_complete).sum():,} with a missing value get the train sale rate {base_rate:.3f}")

SUBMISSIONS.mkdir(exist_ok=True)
out = SUBMISSIONS / "baseline.csv"
pd.DataFrame({"id": test.id, TARGET: p}).to_csv(out, index=False)
print(f"written {out}  ({date.today()})")
