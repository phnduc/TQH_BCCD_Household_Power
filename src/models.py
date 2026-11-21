"""Khối E — Mô hình phân lớp mức phụ tải và hồi quy dự báo công suất (chủ: DA).

Bao gồm các mô hình:
- Phân lớp mức phụ tải (DecisionTree, KNN, LogisticRegression).
- Hồi quy dự báo công suất tác dụng (DecisionTreeRegressor, LinearRegression).
Kiểm định chéo phân tầng K-Fold trên tập huấn luyện, tinh chỉnh siêu tham số bằng GridSearchCV.
"""
from __future__ import annotations

import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import GridSearchCV, KFold, StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

from src import config

CLS_SCORING = {"f1_macro": "f1_macro"}
REG_SCORING = {"rmse": "neg_root_mean_squared_error"}


def _is_regression(y: pd.Series) -> bool:
    return pd.api.types.is_numeric_dtype(y)


def _estimator(name: str, regression: bool) -> BaseEstimator:
    if regression:
        if name == "decision_tree":
            return DecisionTreeRegressor(random_state=config.SEED)
        if name == "linear_regression":
            return Pipeline([("scale", StandardScaler()), ("model", LinearRegression())])
    else:
        if name == "decision_tree":
            return DecisionTreeClassifier(random_state=config.SEED)
        if name == "knn":
            return Pipeline([("scale", StandardScaler()), ("model", KNeighborsClassifier())])
        if name == "logistic_regression":
            return Pipeline([
                ("scale", StandardScaler()),
                ("model", LogisticRegression(max_iter=config.LOGREG_MAX_ITER, random_state=config.SEED))
            ])
    raise ValueError(f"Mô hình {name!r} không nằm trong danh mục config")


def _grid_for(name: str, regression: bool) -> dict:
    grid = (config.REGRESSOR_GRID if regression else config.CLASSIFIER_GRID)[name]
    needs_prefix = name in ("knn", "logistic_regression", "linear_regression")
    return {(f"model__{k}" if needs_prefix else k): v for k, v in grid.items()}


def _cv(regression: bool):
    cls = KFold if regression else StratifiedKFold
    return cls(n_splits=config.CV_FOLDS, shuffle=False)


def tune(model_name: str, x_train: pd.DataFrame, y_train: pd.Series) -> object:
    """Tìm kiếm siêu tham số tối ưu trên tập huấn luyện bằng GridSearchCV."""
    regression = _is_regression(y_train)
    scoring = (REG_SCORING if regression else CLS_SCORING)[
        config.PRIMARY_METRIC_REG if regression else config.PRIMARY_METRIC_CLS
    ]
    search = GridSearchCV(
        _estimator(model_name, regression),
        _grid_for(model_name, regression),
        scoring=scoring,
        cv=_cv(regression),
        n_jobs=2,   # dùng 2 CPU core (không đốt hết máy)
        refit=True
    )
    return search.fit(x_train, y_train)


def train_classifiers(x_train: pd.DataFrame, y_train: pd.Series) -> dict[str, object]:
    """Huấn luyện các mô hình phân lớp được định nghĩa trong config.CLASSIFIER_GRID."""
    return {name: tune(name, x_train, y_train) for name in config.CLASSIFIER_GRID}


def train_regressors(x_train: pd.DataFrame, y_train: pd.Series) -> dict[str, object]:
    """Huấn luyện các mô hình hồi quy được định nghĩa trong config.REGRESSOR_GRID."""
    return {name: tune(name, x_train, y_train) for name in config.REGRESSOR_GRID}
