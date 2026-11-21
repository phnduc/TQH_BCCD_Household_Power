"""Khối F — Phân cụm hồ sơ phụ tải điện (chủ: DA).

Áp dụng thuật toán k-means để gom cụm các hồ sơ phụ tải tiêu thụ điện theo ngày (Daily Load Profiles),
sử dụng phương pháp khuỷu tay (elbow) và hệ số Silhouette để lựa chọn số cụm k tối ưu.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

from src import config


def choose_k(x: pd.DataFrame) -> pd.DataFrame:
    """Đánh giá quán tính (inertia) và hệ số silhouette cho k từ config.KMEANS_K_MIN đến config.KMEANS_K_MAX."""
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)

    rows = []
    for k in range(config.KMEANS_K_MIN, config.KMEANS_K_MAX + 1):
        km = KMeans(n_clusters=k, random_state=config.SEED, n_init=config.N_KMEANS_INIT)
        labels = km.fit_predict(x_scaled)
        sil = silhouette_score(x_scaled, labels) if k > 1 else np.nan
        rows.append({"k": k, "inertia": km.inertia_, "silhouette": sil})

    return pd.DataFrame(rows)


def fit_clusters(x: pd.DataFrame, k: int) -> np.ndarray:
    """Khớp mô hình k-means với số cụm k và hạt giống SEED từ config; trả về mảng nhãn cụm."""
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)
    km = KMeans(n_clusters=k, random_state=config.SEED, n_init=config.N_KMEANS_INIT)
    return km.fit_predict(x_scaled)


def crosstab_with_load_type(labels: np.ndarray, load_type: pd.Series) -> pd.DataFrame:
    """Bảng chéo đối chiếu phân bố giữa nhãn cụm phân cụm và mức phụ tải thực tế."""
    df = pd.DataFrame({"cum": labels, "load_type": load_type.reset_index(drop=True)})
    return pd.crosstab(df["cum"], df["load_type"], margins=True)
