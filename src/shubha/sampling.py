"""Build the working sample and the held-out test set from the PaySim data.

Why two sets?
- Fraud is very rare (about 0.13% of PaySim rows). Training on the raw data would
  teach the model to always say "not fraud".
- So the TRAIN sample keeps every fraud row and only a random subset of legitimate
  rows (under-sampling). This makes fraud easier to learn.
- The TEST set is the opposite: it keeps the natural, very low fraud rate, so our
  precision, recall and F1 numbers reflect what would happen in real life.
- The test set is cut out FIRST, so no row ever appears in both sets (no leakage).

Usage (from the project root):
    python -m shubha.sampling --input data/raw/paysim.csv --out data/processed
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

LABEL_COLUMN = "isFraud"


def check_columns(df: pd.DataFrame) -> None:
    """Stop early with a clear message if the label column is missing."""
    if LABEL_COLUMN not in df.columns:
        raise ValueError(f"Column '{LABEL_COLUMN}' not found in the data")


def stratified_split(df: pd.DataFrame, test_fraction: float, seed: int):
    """Split df into (pool, test) keeping the same fraud rate in both parts.

    We split fraud rows and legitimate rows separately, so the test set gets
    the same share of fraud as the whole data (a "stratified" split).
    """
    check_columns(df)
    if not 0 < test_fraction < 1:
        raise ValueError("test_fraction must be between 0 and 1")

    rng = np.random.default_rng(seed)
    test_parts = []
    for _, group in df.groupby(LABEL_COLUMN):
        n_test = int(round(len(group) * test_fraction))
        # choose n_test row positions at random, without repeating any row
        chosen = rng.choice(len(group), size=n_test, replace=False)
        test_parts.append(group.iloc[chosen])

    test = pd.concat(test_parts).sort_index()
    pool = df.drop(index=test.index)
    return pool, test


def undersample(pool: pd.DataFrame, n_legit: int, seed: int) -> pd.DataFrame:
    """Keep ALL fraud rows and at most n_legit random legitimate rows."""
    check_columns(pool)
    fraud = pool[pool[LABEL_COLUMN] == 1]
    legit = pool[pool[LABEL_COLUMN] == 0]
    # if there are fewer legit rows than requested, just keep them all
    n_keep = min(n_legit, len(legit))
    legit_sample = legit.sample(n=n_keep, random_state=seed)
    return pd.concat([fraud, legit_sample]).sort_index()


def build_sample(df: pd.DataFrame, n_legit: int = 100_000,
                 test_fraction: float = 0.2, seed: int = 42):
    """Return (train_sample, test_natural).

    1. Cut a test set at the natural fraud rate.
    2. From the rest, keep all fraud + n_legit legitimate rows.
    """
    pool, test = stratified_split(df, test_fraction, seed)
    train = undersample(pool, n_legit, seed)
    return train, test


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--input", required=True, help="path to the (cleaned) CSV")
    parser.add_argument("--out", default="data/processed", help="output folder")
    parser.add_argument("--n-legit", type=int, default=100_000)
    parser.add_argument("--test-fraction", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    train, test = build_sample(df, args.n_legit, args.test_fraction, args.seed)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    train.to_csv(out_dir / "train_sample.csv", index=False)
    test.to_csv(out_dir / "test_natural.csv", index=False)

    print(f"train_sample: {len(train):,} rows, fraud rate {train[LABEL_COLUMN].mean():.4%}")
    print(f"test_natural: {len(test):,} rows, fraud rate {test[LABEL_COLUMN].mean():.4%}")


if __name__ == "__main__":
    main()
