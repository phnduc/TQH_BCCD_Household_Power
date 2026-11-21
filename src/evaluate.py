"""Khối G — Độ đo đánh giá hiệu năng và phân tích lỗi mô hình (chủ: DA).

Tính toán các độ đo: Precision, Recall, F1 macro từng lớp, Accuracy, MAE, RMSE, R2,
phân tích ma trận nhầm lẫn và lỗi dự báo theo giờ và loại ngày.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    mean_absolute_error,
    mean_squared_error,
    precision_recall_fscore_support,
    r2_score,
)


def classification_report_table(y_true, y_pred, labels: list[str]) -> pd.DataFrame:
    """Bảng đánh giá phân lớp chi tiết theo từng lớp (Precision, Recall, F1, Support) và trung bình macro."""
    p, r, f, s = precision_recall_fscore_support(y_true, y_pred, labels=labels, zero_division=0)
    table = pd.DataFrame({"lop": labels, "precision": p, "recall": r, "f1": f, "support": s})
    macro = {
        "lop": "macro_avg",
        "precision": p.mean(),
        "recall": r.mean(),
        "f1": f.mean(),
        "support": int(s.sum()),
    }
    acc = {
        "lop": "accuracy",
        "precision": np.nan,
        "recall": np.nan,
        "f1": accuracy_score(y_true, y_pred),
        "support": int(s.sum()),
    }
    return pd.concat([table, pd.DataFrame([macro, acc])], ignore_index=True)


def regression_report(y_true, y_pred) -> dict[str, float]:
    """Báo cáo chỉ số hồi quy đánh giá dự báo phụ tải: MAE, RMSE, R2."""
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "r2": float(r2_score(y_true, y_pred)),
    }


def top_confusions(y_true, y_pred, labels: list[str]) -> pd.DataFrame:
    """Liệt kê các cặp nhầm lẫn giữa nhãn thực tế và nhãn dự đoán sắp xếp giảm dần."""
    t, p = np.asarray(y_true), np.asarray(y_pred)
    rows = []
    for a in labels:
        n_a = int((t == a).sum())
        for b in labels:
            if a != b:
                n = int(((t == a) & (p == b)).sum())
                rows.append({
                    "that": a,
                    "doan": b,
                    "so_luong": n,
                    "ti_le_tren_lop_that": n / n_a if n_a else 0.0,
                })
    return pd.DataFrame(rows).sort_values("so_luong", ascending=False, ignore_index=True)


def error_by_group(y_true, y_pred, groups) -> pd.DataFrame:
    """Phân tích độ chính xác theo từng nhóm (giờ trong ngày, ngày trong tuần) để khoanh vùng lỗi."""
    df = pd.DataFrame({"nhom": np.asarray(groups), "dung": np.asarray(y_true) == np.asarray(y_pred)})
    g = df.groupby("nhom")["dung"].agg(["mean", "size"]).reset_index()
    return g.rename(columns={"mean": "accuracy", "size": "so_mau"})


def feature_importance_table(model, feature_names: list[str]) -> pd.DataFrame:
    """Trích xuất độ quan trọng của các đặc trưng phụ tải từ mô hình dạng cây."""
    est = getattr(model, "best_estimator_", model)
    imp = getattr(est, "feature_importances_", None)
    if imp is None:
        raise ValueError("Mô hình không hỗ trợ trích xuất feature_importances_")
    return pd.DataFrame({"dac_trung": feature_names, "do_quan_trong": imp}).sort_values(
        "do_quan_trong", ascending=False, ignore_index=True
    )
