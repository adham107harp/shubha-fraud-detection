import numpy as np
import pandas as pd
import pytest

from shubha.sampling import build_sample, stratified_split


def make_data(n=10_000, fraud_rate=0.01, seed=0):
    """Tiny fake transactions table with a known fraud rate."""
    rng = np.random.default_rng(seed)
    n_fraud = int(n * fraud_rate)
    labels = np.array([1] * n_fraud + [0] * (n - n_fraud))
    rng.shuffle(labels)
    return pd.DataFrame({
        "step": rng.integers(1, 700, n),
        "type": rng.choice(["TRANSFER", "CASH_OUT", "PAYMENT"], n),
        "amount": rng.lognormal(mean=9, sigma=1, size=n),
        "isFraud": labels,
    })


def test_train_keeps_all_fraud_and_limits_legit():
    df = make_data()
    pool, _ = stratified_split(df, test_fraction=0.2, seed=1)
    train, _ = build_sample(df, n_legit=500, test_fraction=0.2, seed=1)

    # every fraud row that is not in the test set must be in the train sample
    assert train["isFraud"].sum() == pool["isFraud"].sum()
    # and exactly n_legit legitimate rows were kept
    assert (train["isFraud"] == 0).sum() == 500


def test_train_and_test_never_share_a_row():
    df = make_data()
    train, test = build_sample(df, n_legit=500, test_fraction=0.2, seed=1)
    # if the two index sets overlap, test data leaked into training
    assert set(train.index).isdisjoint(set(test.index))


def test_test_set_keeps_natural_fraud_rate():
    df = make_data(n=20_000, fraud_rate=0.01)
    _, test = build_sample(df, n_legit=500, test_fraction=0.2, seed=1)
    # the test set should look like the real data: about 1% fraud
    assert test["isFraud"].mean() == pytest.approx(df["isFraud"].mean(), abs=0.002)


def test_same_seed_gives_same_result():
    df = make_data()
    train_a, test_a = build_sample(df, n_legit=500, seed=7)
    train_b, test_b = build_sample(df, n_legit=500, seed=7)
    assert train_a.index.equals(train_b.index)
    assert test_a.index.equals(test_b.index)


def test_missing_label_column_raises_clear_error():
    df = make_data().drop(columns=["isFraud"])
    with pytest.raises(ValueError, match="isFraud"):
        build_sample(df)
