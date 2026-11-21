"""Khối C — Trực quan hóa dữ liệu phụ tải điện (chủ: Sơn).

Mỗi hàm lưu biểu đồ vào config.FIG_DIR theo quy ước chuẩn và trả về đường dẫn tệp.
Mỗi biểu đồ bắt buộc có tiêu đề, nhãn trục, đơn vị đo và nhận xét phân tích.
"""
from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src import config


def _setup_fig_dir() -> Path:
    config.FIG_DIR.mkdir(parents=True, exist_ok=True)
    return config.FIG_DIR


def plot_distribution(df: pd.DataFrame, column: str, by: str | None = None) -> Path:
    """Biểu đồ phân bố công suất hoặc điện năng tiêu thụ, có thể nhóm theo mức phụ tải."""
    d = _setup_fig_dir()
    plt.figure(figsize=(8, 5))
    if by and by in df.columns:
        for val in df[by].dropna().unique():
            sub = df[df[by] == val][column].dropna()
            plt.hist(sub, bins=30, alpha=0.5, label=str(val), density=True)
        plt.legend(title=by)
    else:
        plt.hist(df[column].dropna(), bins=30, color="steelblue", edgecolor="black", alpha=0.7)

    plt.title(f"Phân bố thuộc tính {column}")
    plt.xlabel(f"{column} (kW hoặc Wh)")
    plt.ylabel("Mật độ phân bố")
    plt.tight_layout()
    out = d / f"c_01_phan_bo_{column}.png"
    plt.savefig(out, dpi=200)
    plt.close()
    return out


def plot_heatmap_hour_weekday(df: pd.DataFrame) -> Path:
    """Bản đồ nhiệt (heatmap) mức tiêu thụ phụ tải trung bình theo Giờ trong ngày x Thứ trong tuần."""
    d = _setup_fig_dir()
    pivot = df.pivot_table(
        index="hour",
        columns="day_of_week",
        values=config.TARGET_REG,
        aggfunc="mean"
    )
    plt.figure(figsize=(9, 6))
    plt.imshow(pivot, aspect="auto", cmap="YlOrRd", origin="lower")
    plt.colorbar(label="Công suất tác dụng trung bình (kW)")
    plt.xticks(ticks=range(len(pivot.columns)), labels=pivot.columns, rotation=45)
    plt.yticks(ticks=range(len(pivot.index)), labels=pivot.index)
    plt.title("Bản đồ nhiệt phụ tải điện: Giờ x Thứ trong tuần")
    plt.xlabel("Thứ trong tuần")
    plt.ylabel("Giờ trong ngày (0 - 23h)")
    plt.tight_layout()
    out = d / "c_02_heatmap_gio_thu.png"
    plt.savefig(out, dpi=200)
    plt.close()
    return out


def plot_scatter(df: pd.DataFrame, x: str, y: str, hue: str | None = None) -> Path:
    """Biểu đồ tán xạ (scatter plot) quan hệ giữa hai đại lượng đo lường phụ tải."""
    d = _setup_fig_dir()
    plt.figure(figsize=(8, 5))
    if hue and hue in df.columns:
        for val in df[hue].dropna().unique():
            sub = df[df[hue] == val]
            plt.scatter(sub[x], sub[y], alpha=0.4, label=str(val), s=15)
        plt.legend(title=hue)
    else:
        plt.scatter(df[x], df[y], alpha=0.4, color="coral", s=15)

    plt.title(f"Biểu đồ tán xạ quan hệ giữa {x} và {y}")
    plt.xlabel(x)
    plt.ylabel(y)
    plt.tight_layout()
    out = d / f"c_03_tan_xa_{x}_{y}.png"
    plt.savefig(out, dpi=200)
    plt.close()
    return out


def plot_corr_matrix(df: pd.DataFrame) -> Path:
    """Ma trận tương quan giữa các đại lượng đo điện năng tiêu thụ."""
    d = _setup_fig_dir()
    num_cols = [c for c in config.FEATURE_COLS_NUMERIC + [config.TARGET_REG] if c in df.columns]
    corr = df[num_cols].corr()

    plt.figure(figsize=(8, 7))
    plt.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    plt.colorbar(label="Hệ số tương quan Pearson")
    plt.xticks(range(len(num_cols)), num_cols, rotation=45, ha="right")
    plt.yticks(range(len(num_cols)), num_cols)
    plt.title("Ma trận tương quan giữa các đại lượng phụ tải điện")
    plt.tight_layout()
    out = d / "c_04_ma_tran_tuong_quan.png"
    plt.savefig(out, dpi=200)
    plt.close()
    return out


def plot_confusion_matrix(y_true, y_pred, labels: list[str], name: str) -> Path:
    """Trực quan hóa ma trận nhầm lẫn (Confusion Matrix) của mô hình phân lớp."""
    d = _setup_fig_dir()
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y_true, y_pred, labels=labels)

    plt.figure(figsize=(6, 5))
    plt.imshow(cm, cmap="Blues")
    plt.colorbar(label="Số mẫu")
    plt.xticks(range(len(labels)), labels, rotation=45)
    plt.yticks(range(len(labels)), labels)
    for i in range(len(labels)):
        for j in range(len(labels)):
            plt.text(j, i, str(cm[i, j]), ha="center", va="center", color="black" if cm[i, j] < cm.max()/2 else "white")
    plt.title(f"Ma trận nhầm lẫn mô hình {name}")
    plt.xlabel("Nhãn dự đoán")
    plt.ylabel("Nhãn thực tế")
    plt.tight_layout()
    out = d / f"c_05_confusion_{name}.png"
    plt.savefig(out, dpi=200)
    plt.close()
    return out
