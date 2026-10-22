"""Check a submission file before uploading it.

Usage: uv run python -m kit.check_submission submissions/<file>.csv
Exits with an error on anything Kaggle would reject; prints warnings for things Kaggle accepts but will punish.
"""
import sys
import numpy as np, pandas as pd
from kit.data import DATA, TARGET, N_TEST


def check(path) -> pd.DataFrame:
    errors, warnings = [], []
    sub = pd.read_csv(path)
    test_ids = pd.read_csv(DATA / "test.csv", usecols=["id"]).id

    if list(sub.columns) != ["id", TARGET]:
        errors.append(f"columns must be exactly ['id', '{TARGET}'], got {list(sub.columns)}")
    else:
        if len(sub) != N_TEST:
            errors.append(f"{len(sub):,} rows, expected {N_TEST:,}")
        if sub.id.duplicated().any():
            errors.append(f"{sub.id.duplicated().sum()} duplicated ids")
        if set(sub.id) != set(test_ids):
            errors.append(f"ids differ from test.csv: {len(set(test_ids) - set(sub.id))} missing, {len(set(sub.id) - set(test_ids))} unknown")
        p = pd.to_numeric(sub[TARGET], errors="coerce")
        if p.isna().any():
            errors.append(f"{p.isna().sum()} missing or non-numeric predictions")
        else:
            if (p < 0).any() or (p > 1).any():
                errors.append(f"predictions outside [0, 1]: min {p.min():.4f}, max {p.max():.4f}")
            if ((p == 0) | (p == 1)).any():
                warnings.append(f"{((p == 0) | (p == 1)).sum()} predictions are exactly 0 or 1: one wrong costs about 36 in log loss")
            elif p.min() < 0.01 or p.max() > 0.99:
                warnings.append(f"very confident predictions (min {p.min():.4f}, max {p.max():.4f}): are you sure? clipping to [0.01, 0.99] is cheap insurance")
            if p.nunique() == 1:
                warnings.append("every prediction is the same value")
            print(f"{len(sub):,} rows; mean prediction {p.mean():.3f} (train sale rate 0.397); min {p.min():.3f}, max {p.max():.3f}")

    for w in warnings:
        print(f"WARNING: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    if errors:
        sys.exit(1)
    print(f"OK: {path} is a valid submission")
    return sub


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    check(sys.argv[1])
