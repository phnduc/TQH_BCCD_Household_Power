"""Khối B — Giảm chiều dữ liệu và xếp hạng thuộc tính (chủ: Duy).

Sử dụng PCA để giảm số chiều không gian đặc trưng và xếp hạng độ quan trọng
của các biến phụ tải đối với mức tiêu thụ điện năng.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

from src import config


def pca_reduce(x_train: pd.DataFrame, x_test: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, object]:
    """Giảm chiều dữ liệu bằng PCA: khớp trên train, giữ phương sai tích lũy tối thiểu config.PCA_VARIANCE."""
    scaler = StandardScaler()
    x_tr_scaled = scaler.fit_transform(x_train)
    x_te_scaled = scaler.transform(x_test)

    pca = PCA(n_components=config.PCA_VARIANCE, random_state=config.SEED)
    train_z = pca.fit_transform(x_tr_scaled)
    test_z = pca.transform(x_te_scaled)
    return train_z, test_z, pca


def rank_features(x_train: pd.DataFrame, y_train: pd.Series) -> pd.DataFrame:
    """Xếp hạng độ quan trọng của các thuộc tính dựa trên mô hình học máy dạng cây."""
    model = RandomForestRegressor(n_estimators=50, random_state=config.SEED)
    model.fit(x_train, y_train)
    scores = model.feature_importances_
    return pd.DataFrame({"dac_trung": x_train.columns, "diem": scores}).sort_values(
        "diem", ascending=False, ignore_index=True
    )
