"""Khối B — Dữ liệu và tiền xử lý (chủ: Đức).

Tập dữ liệu tiêu thụ điện hộ gia đình (UCI Individual Household Electric Power Consumption).
Xử lý dữ liệu chuỗi thời gian, giá trị khuyết thiếu '?', phát hiện ngoại lai,
chia tập theo thứ tự thời gian để tránh rò rỉ (data leakage).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from src import config

HOUR_COL = "hour"
MONTH_COL = "month"
OUTLIER_COL = "is_outlier"


def load_raw() -> pd.DataFrame:
    """Đọc dữ liệu thô từ data/raw/<DATA_LOCAL_NAME>.
    
    UCI Household Power Consumption là tệp CSV/TXT phân tách bằng dấu chấm phẩy (;),
    các giá trị khuyết thiếu ký hiệu là '?'.
    """
    path = config.RAW_DIR / config.DATA_LOCAL_NAME
    if not path.exists():
        raise FileNotFoundError(f"Thiếu {path}; hãy chạy: python data/download_data.py")
    
    # Đọc dữ liệu với ký hiệu giá trị thiếu '?'
    df = pd.read_csv(
        path,
        sep=";",
        na_values=["?"],
        low_memory=False,
    )
    if df.shape[1] != config.EXPECTED_COLS:
        raise ValueError(f"Số cột không khớp: {df.shape[1]}, kỳ vọng {config.EXPECTED_COLS}")
    return df


def _numeric_cols(df: pd.DataFrame) -> list[str]:
    return [
        c for c in df.columns
        if pd.api.types.is_numeric_dtype(df[c])
        and not pd.api.types.is_bool_dtype(df[c])
        and c not in (HOUR_COL, MONTH_COL)
    ]


def _iqr_outlier_mask(df: pd.DataFrame, col: str) -> pd.Series:
    """Xác định ngoại lai theo quy tắc 1.5 x IQR."""
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    return (df[col] < q1 - config.IQR_K * iqr) | (df[col] > q3 + config.IQR_K * iqr)


def _nonsense_mask(df: pd.DataFrame) -> pd.Series:
    """Kiểm tra các giá trị vi phạm giới hạn vật lý."""
    bad = pd.Series(False, index=df.index)
    if "Voltage" in df.columns:
        bad |= (df["Voltage"] < config.VOLTAGE_RANGE[0]) | (df["Voltage"] > config.VOLTAGE_RANGE[1])
    for col in ("Global_active_power", "Global_reactive_power"):
        if col in df.columns:
            bad |= df[col] < config.POWER_MIN
    return bad


def quality_report(df: pd.DataFrame) -> pd.DataFrame:
    """Báo cáo chất lượng dữ liệu: số lượng khuyết thiếu, ngoại lai IQR, bản ghi trùng lặp và vô lý."""
    rows = []
    for col in df.columns:
        row = {"muc": col, "thieu": int(df[col].isna().sum()), "ngoai_lai_iqr": None}
        if (
            pd.api.types.is_numeric_dtype(df[col])
            and not pd.api.types.is_bool_dtype(df[col])
        ):
            row["ngoai_lai_iqr"] = int(_iqr_outlier_mask(df, col).sum())
        rows.append(row)
    rows.append({"muc": "[tong] dong_trung_lap", "thieu": int(df.duplicated().sum()), "ngoai_lai_iqr": None})
    rows.append({"muc": "[tong] dong_vo_ly", "thieu": int(_nonsense_mask(df).sum()), "ngoai_lai_iqr": None})
    rows.append({"muc": "[tong] so_dong", "thieu": len(df), "ngoai_lai_iqr": None})
    return pd.DataFrame(rows)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Làm sạch dữ liệu, xử lý giá trị thiếu, tạo đặc trưng thời gian và phân loại mức phụ tải.
    
    1. Ghép Date và Time thành Datetime.
    2. Điền giá trị thiếu (forward-fill / nội suy cho chuỗi thời gian).
    3. Tính năng lượng tiêu thụ phụ tải còn lại (Sub_metering_remainder).
    4. Gán nhãn phân lớp Load_Level (Low_Load, Normal_Load, Peak_Load).
    5. Đánh dấu ngoại lai theo IQR (không xóa, chỉ flag).
    """
    out = df.drop_duplicates().copy()
    
    # Kết hợp Date và Time thành cột thời gian thống nhất
    if config.DATETIME_COL not in out.columns:
        if config.DATE_COL in out.columns and config.TIME_COL in out.columns:
            out[config.DATETIME_COL] = pd.to_datetime(
                out[config.DATE_COL].astype(str) + " " + out[config.TIME_COL].astype(str),
                format=f"{config.DATE_FORMAT} {config.TIME_FORMAT}",
                errors="coerce"
            )
            out = out.dropna(subset=[config.DATETIME_COL]).sort_values(config.DATETIME_COL)

    # Chuyển các cột đo lường sang kiểu float
    num_cols = [
        "Global_active_power", "Global_reactive_power", "Voltage",
        "Global_intensity", "Sub_metering_1", "Sub_metering_2", "Sub_metering_3"
    ]
    for col in num_cols:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
            # Điền khuyết thiếu cho chuỗi thời gian bằng forward-fill rồi backward-fill
            out[col] = out[col].ffill().bfill()

    # Loại bỏ bản ghi vi phạm ngưỡng vật lý
    out = out.loc[~_nonsense_mask(out)].copy()

    # Tính toán đặc trưng thời gian
    dt = out[config.DATETIME_COL]
    out[HOUR_COL] = dt.dt.hour
    out[MONTH_COL] = dt.dt.month
    out["day_of_week"] = dt.dt.day_name()
    out["is_weekend"] = dt.dt.dayofweek.isin([5, 6]).astype(int)

    # Tính Sub_metering_remainder (Wh mỗi phút):
    # Total active energy = Global_active_power * 1000 / 60
    # Remainder = Total - (Sub_metering_1 + Sub_metering_2 + Sub_metering_3)
    if "Global_active_power" in out.columns and "Sub_metering_1" in out.columns:
        active_wh = out["Global_active_power"] * 1000.0 / 60.0
        remainder = active_wh - (out["Sub_metering_1"] + out["Sub_metering_2"] + out["Sub_metering_3"])
        out["Sub_metering_remainder"] = np.maximum(remainder, 0.0)

    # Gán nhãn phân lớp mức phụ tải Load_Level theo tam phân vị
    if config.TARGET_REG in out.columns and config.TARGET_CLS not in out.columns:
        p33 = out[config.TARGET_REG].quantile(1.0 / 3.0)
        p67 = out[config.TARGET_REG].quantile(2.0 / 3.0)
        out[config.TARGET_CLS] = np.where(
            out[config.TARGET_REG] <= p33,
            config.LOAD_CLASSES[0],
            np.where(out[config.TARGET_REG] <= p67, config.LOAD_CLASSES[1], config.LOAD_CLASSES[2])
        )

    # Đánh dấu ngoại lai
    flag = pd.Series(False, index=out.index)
    for col in (c for c in _numeric_cols(out) if c in out.columns):
        flag |= _iqr_outlier_mask(out, col)
    out[OUTLIER_COL] = flag

    if config.OUTLIER_POLICY == "drop":
        out = out.loc[~out[OUTLIER_COL]].copy()

    return out.reset_index(drop=True)


def time_split(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Chia tập dữ liệu theo thứ tự thời gian thành (train, test) để tránh data leakage."""
    if config.SPLIT_MODE != "time":
        raise ValueError(f"SPLIT_MODE={config.SPLIT_MODE!r} không được hỗ trợ")
    cut = int(round(len(df) * (1 - config.TEST_FRACTION)))
    return df.iloc[:cut].copy(), df.iloc[cut:].copy()


def save_clean(df: pd.DataFrame) -> None:
    """Lưu dữ liệu sạch ra tệp riêng data/clean/."""
    config.CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(config.CLEAN_DIR / config.CLEAN_DATA_NAME, index=False)


def feature_columns(task: str) -> list[str]:
    """Danh sách cột đặc trưng đầu vào cho 'cls' hoặc 'reg', loại bỏ biến rò rỉ và biến mục tiêu."""
    if task not in ("cls", "reg"):
        raise ValueError("task phải là 'cls' hoặc 'reg'")
    banned = set(config.LEAKY_COLS) | set(config.CLS_EXCLUDE_COLS if task == "cls" else config.REG_EXCLUDE_COLS)
    
    candidates = config.FEATURE_COLS_NUMERIC + config.FEATURE_COLS_CATEGORICAL
    return [c for c in candidates if c not in banned]


def make_features(train: pd.DataFrame, test: pd.DataFrame, task: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Mã hóa đặc trưng One-Hot cho các cột phân loại, khớp chuẩn hóa/cột trên train và áp lên test."""
    cols = feature_columns(task)
    cat_cols = [c for c in cols if c in config.FEATURE_COLS_CATEGORICAL]
    
    tr = pd.get_dummies(train[cols], columns=cat_cols, drop_first=True)
    te = pd.get_dummies(test[cols], columns=cat_cols, drop_first=True)
    
    # Đồng bộ hóa các cột giữa train và test
    tr, te = tr.align(te, join="left", axis=1, fill_value=0)
    return tr.astype(float), te.astype(float)


def add_lag_features(df: pd.DataFrame) -> pd.DataFrame:
    """Tạo đặc trưng trễ (lags) của phụ tải cho bài toán dự báo chuỗi thời gian."""
    out = df.copy()
    for lag in config.LAG_STEPS:
        out[f"lag_{lag}_{config.TARGET_REG}"] = out[config.TARGET_REG].shift(lag)
    return out.bfill()


def lag_feature_names() -> list[str]:
    """Tên các cột đặc trưng trễ."""
    return [f"lag_{lag}_{config.TARGET_REG}" for lag in config.LAG_STEPS]
