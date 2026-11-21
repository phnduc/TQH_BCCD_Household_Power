"""Kiểm các quyết định thiết kế đã chốt cho đề tài phụ tải điện hộ gia đình."""
from src import config


def test_classifiers_meet_spec():
    assert len(config.CLASSIFIER_GRID) >= 3
    assert all(isinstance(v, dict) for v in config.CLASSIFIER_GRID.values())
    assert any(grid for grid in config.CLASSIFIER_GRID.values())


def test_regressor_defined():
    assert config.REGRESSOR_GRID


def test_metrics_and_policies():
    assert config.PRIMARY_METRIC_CLS == "f1_macro"
    assert config.PRIMARY_METRIC_REG == "rmse"
    assert config.OUTLIER_POLICY in {"flag", "drop"}
    assert config.SAMPLING == "none"


def test_hour_bins_cover_a_day():
    e = config.HOUR_BIN_EDGES
    assert list(e) == sorted(e) and e[0] == 0 and e[-1] == 24


def test_discretize_levels_and_seed():
    assert len(config.DISCRETIZE_LEVELS) == 3
    assert config.SEED == 4759 and config.N_KMEANS_INIT >= 1
