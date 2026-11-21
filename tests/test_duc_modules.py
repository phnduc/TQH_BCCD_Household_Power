"""Kiểm data_prep, models, evaluate trên dữ liệu tổng hợp nhỏ mô phỏng phụ tải hộ gia đình."""
import numpy as np
import pandas as pd
import pytest

from src import config, data_prep, evaluate, models


def _fake_household_data(n=240):
    rng = np.random.default_rng(config.SEED)
    t = pd.date_range("2007-01-01 00:00", periods=n, freq=config.RESAMPLE_FREQ)
    active = rng.gamma(2.0, 1.2, n)
    reactive = rng.uniform(0.05, 0.4, n)
    voltage = rng.normal(240.0, 3.0, n)
    intensity = (active * 1000.0) / voltage
    sub1 = np.where(rng.random(n) < 0.2, rng.uniform(5, 30, n), 0.0)
    sub2 = np.where(rng.random(n) < 0.3, rng.uniform(5, 25, n), 0.0)
    sub3 = np.where(rng.random(n) < 0.5, rng.uniform(10, 40, n), 0.0)

    return pd.DataFrame({
        config.DATE_COL: t.strftime(config.DATE_FORMAT),
        config.TIME_COL: t.strftime(config.TIME_FORMAT),
        "Global_active_power": active,
        "Global_reactive_power": reactive,
        "Voltage": voltage,
        "Global_intensity": intensity,
        "Sub_metering_1": sub1,
        "Sub_metering_2": sub2,
        "Sub_metering_3": sub3,
    })


def test_clean_keeps_order_and_adds_features():
    raw = _fake_household_data()
    out = data_prep.clean(raw)
    assert len(out) == len(raw)
    assert out[config.DATETIME_COL].is_monotonic_increasing
    assert {"hour", "month", "day_of_week", "is_weekend", "Sub_metering_remainder", "Load_Level", "is_outlier"} <= set(out.columns)


def test_clean_drops_duplicates_and_nonsense():
    raw = _fake_household_data()
    bad = raw.iloc[[0]].copy()
    bad["Voltage"] = 150.0  # Vi phạm dải điện áp
    out = data_prep.clean(pd.concat([raw, raw.iloc[[5]], bad], ignore_index=True))
    assert len(out) == len(raw)


def test_time_split_is_ordered_and_sized():
    out = data_prep.clean(_fake_household_data())
    train, test = data_prep.time_split(out)
    assert len(train) + len(test) == len(out)
    assert abs(len(test) / len(out) - config.TEST_FRACTION) < 0.01
    assert train[config.DATETIME_COL].max() < test[config.DATETIME_COL].min()


def test_models_train_and_predict():
    out = data_prep.clean(_fake_household_data(n=120))
    train, test = data_prep.time_split(out)
    xc_tr, xc_te = data_prep.make_features(train, test, "cls")
    clfs = models.train_classifiers(xc_tr, train[config.TARGET_CLS])
    assert "decision_tree" in clfs
    pred = clfs["decision_tree"].predict(xc_te)
    rep = evaluate.classification_report_table(test[config.TARGET_CLS], pred, config.LOAD_CLASSES)
    assert not rep.empty
