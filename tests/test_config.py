"""Kiểm cấu hình: đúng với đề tài phân tích và dự báo phụ tải điện hộ gia đình."""
from src import config


def test_group_and_topic():
    assert config.GROUP_ID == 1
    assert config.CLASS_CODE == "D18CNPM1"
    assert "phụ tải điện" in config.TOPIC_NAME.lower()


def test_thresholds_sane():
    assert 0 < config.TEST_FRACTION < 1
    assert config.CV_FOLDS >= 2
    assert config.KMEANS_K_MIN >= 2 and config.KMEANS_K_MAX > config.KMEANS_K_MIN
    assert 0 < config.MIN_SUPPORT < 1 and 0 < config.MIN_CONFIDENCE <= 1
    assert config.MIN_FIGURES >= 8 and config.MIN_FIGURE_TYPES >= 4


def test_target_not_in_features():
    feats = set(config.FEATURE_COLS_NUMERIC) | set(config.FEATURE_COLS_CATEGORICAL)
    assert config.TARGET_REG not in feats and config.TARGET_CLS not in feats
    assert not (set(config.LEAKY_COLS) & feats), "Cột rò rỉ không được nằm trong danh sách đặc trưng"
