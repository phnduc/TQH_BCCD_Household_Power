"""Giao diện hàm chuẩn trong src/ (dùng chung, chỉ Đức sửa). Đổi tên hàm hoặc tham số thì test đỏ."""
import importlib
import inspect

import pytest

INTERFACES = {
    "src.data_prep": {
        "load_raw": [],
        "quality_report": ["df"],
        "clean": ["df"],
        "time_split": ["df"],
        "save_clean": ["df"],
    },
    "src.reduce": {
        "pca_reduce": ["x_train", "x_test"],
        "rank_features": ["x_train", "y_train"],
    },
    "src.viz": {
        "plot_distribution": ["df", "column", "by"],
        "plot_heatmap_hour_weekday": ["df"],
        "plot_scatter": ["df", "x", "y", "hue"],
        "plot_corr_matrix": ["df"],
        "plot_confusion_matrix": ["y_true", "y_pred", "labels", "name"],
    },
    "src.assoc": {
        "discretize": ["df"],
        "mine_rules": ["transactions", "consequent_prefix"],
        "correlation_table": ["df"],
    },
    "src.models": {
        "train_classifiers": ["x_train", "y_train"],
        "train_regressors": ["x_train", "y_train"],
        "tune": ["model_name", "x_train", "y_train"],
    },
    "src.clustering": {
        "choose_k": ["x"],
        "fit_clusters": ["x", "k"],
        "crosstab_with_load_type": ["labels", "load_type"],
    },
    "src.evaluate": {
        "classification_report_table": ["y_true", "y_pred", "labels"],
        "regression_report": ["y_true", "y_pred"],
        "top_confusions": ["y_true", "y_pred", "labels"],
    },
}


@pytest.mark.parametrize("module", sorted(INTERFACES))
def test_signatures(module):
    mod = importlib.import_module(module)
    for fn, params in INTERFACES[module].items():
        assert hasattr(mod, fn), f"{module}.{fn} bị xóa hoặc đổi tên"
        got = list(inspect.signature(getattr(mod, fn)).parameters)
        assert got == params, f"{module}.{fn}: tham số {got}, kỳ vọng {params}"
