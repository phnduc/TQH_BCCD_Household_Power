"""Khối D — Mẫu thường xuyên, luật kết hợp và phân tích tương quan (chủ: Duy).

Rời rạc hóa các đại lượng đo lường phụ tải điện hộ gia đình,
áp dụng thuật toán Apriori hoặc FP-Growth để tìm luật kết hợp,
diễn giải mối liên hệ giữa các thiết bị tiêu thụ và mức phụ tải cao điểm.
"""
from __future__ import annotations

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

from src import config


def discretize(df: pd.DataFrame) -> pd.DataFrame:
    """Rời rạc hóa khung giờ, ngày cuối tuần và các phân hệ tiêu thụ Sub_metering thành bảng giao dịch one-hot."""
    out = pd.DataFrame(index=df.index)

    # 1. Khung giờ
    if "hour" in df.columns:
        out["Gio=Dem"] = df["hour"].between(0, 5)
        out["Gio=Sang"] = df["hour"].between(6, 11)
        out["Gio=Chieu"] = df["hour"].between(12, 17)
        out["Gio=Toi"] = df["hour"].between(18, 23)

    # 2. Ngày trong tuần / cuối tuần
    if "is_weekend" in df.columns:
        out["Ngay=CuoiTuan"] = df["is_weekend"] == 1
        out["Ngay=TrongTuan"] = df["is_weekend"] == 0

    # 3. Phân hệ tiêu thụ Sub_metering (Bếp, Giặt, Bình nóng lạnh/Điều hòa)
    for sub in ("Sub_metering_1", "Sub_metering_2", "Sub_metering_3"):
        if sub in df.columns:
            out[f"{sub}=Bat"] = df[sub] > 0.0

    # 4. Mức phụ tải tổng
    if config.TARGET_CLS in df.columns:
        for cls_name in config.LOAD_CLASSES:
            out[f"Load_Level={cls_name}"] = df[config.TARGET_CLS] == cls_name

    return out.astype(bool)


def mine_rules(transactions: pd.DataFrame, consequent_prefix: str = "Load_Level=") -> pd.DataFrame:
    """Khai phá tập mục thường xuyên và luật kết hợp; lọc các luật có vế phải liên quan đến mức phụ tải."""
    frequent_items = apriori(transactions, min_support=config.MIN_SUPPORT, use_colnames=True)
    if frequent_items.empty:
        return pd.DataFrame()

    rules = association_rules(frequent_items, metric="confidence", min_threshold=config.MIN_CONFIDENCE)
    rules = rules[rules["lift"] >= config.MIN_LIFT]

    # Lọc luật có vế phải chứa tiền tố chỉ định
    if consequent_prefix:
        rules = rules[
            rules["consequents"].apply(lambda s: any(consequent_prefix in str(item) for item in s))
        ]

    return rules.sort_values("lift", ascending=False).reset_index(drop=True)


def correlation_table(df: pd.DataFrame) -> pd.DataFrame:
    """Bảng tương quan giữa các đại lượng đo lường phụ tải; đánh dấu các cặp có tương quan rất cao."""
    cols = [c for c in config.FEATURE_COLS_NUMERIC + [config.TARGET_REG] if c in df.columns]
    corr = df[cols].corr()

    records = []
    for i, c1 in enumerate(cols):
        for j, c2 in enumerate(cols):
            if i < j:
                val = corr.loc[c1, c2]
                records.append({
                    "bien_1": c1,
                    "bien_2": c2,
                    "tuong_quan_pearson": val,
                    "trung_thong_tin": abs(val) > 0.90,
                })
    return pd.DataFrame(records).sort_values("tuong_quan_pearson", ascending=False, ignore_index=True)
