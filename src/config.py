"""Cấu hình trung tâm — Đề tài: Phân tích và dự báo phụ tải điện hộ gia đình.

Mọi thông số hệ thống, đường dẫn, ngưỡng phân tích được đặt ở đây;
tuyệt đối không dùng số ma thuật (magic numbers) ở các file khác.
Đổi thông số = thay đổi quyết định nhóm -> ghi vào docs/decisions/README.md.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
CLEAN_DIR = DATA_DIR / "clean"
RESULTS_DIR = ROOT / "results"
FIG_DIR = RESULTS_DIR / "figures"
TABLE_DIR = RESULTS_DIR / "tables"

# --- Thông tin nhóm và hạt giống ngẫu nhiên ----------------------------------------------------
GROUP_ID = 1
CLASS_CODE = "D18CNPM1"
TOPIC_NAME = "Phân tích và dự báo phụ tải điện hộ gia đình"
# Hạt giống cố định theo mã học phần để tái lập 100% kết quả
SEED = 4759

# --- Dữ liệu (UCI Individual Household Electric Power Consumption) -----------------------------
DATA_URL = "https://archive.ics.uci.edu/static/public/235/individual+household+electric+power+consumption.zip"
DATA_LOCAL_NAME = "household_power_consumption.txt"
DATA_SIZE_BYTES: int | None = 132960755
DATA_SHA256: str | None = None

EXPECTED_COLS = 9
# Tổng số bản ghi thô thu thập từng phút từ 16/12/2006 đến 26/11/2010 (47 tháng)
EXPECTED_RAW_ROWS = 2075259

# Định dạng thời gian
DATE_COL = "Date"
TIME_COL = "Time"
DATETIME_COL = "Datetime"
DATE_FORMAT = "%d/%m/%Y"
TIME_FORMAT = "%H:%M:%S"

# Tần số tổng hợp/resample để phân tích chuỗi thời gian phụ tải (15 phút khớp 96 mốc/ngày)
RESAMPLE_FREQ = "15min"

# Mục tiêu dự báo và phân lớp
TARGET_REG = "Global_active_power"  # Công suất tác dụng toàn hộ gia đình (kW)
TARGET_CLS = "Load_Level"           # Mức phụ tải: Low_Load, Normal_Load, Peak_Load

# 3 mức phụ tải phân lớp
LOAD_CLASSES = ["Low_Load", "Normal_Load", "Peak_Load"]

# Các cột đặc trưng số học
FEATURE_COLS_NUMERIC = [
    "Global_reactive_power",  # Công suất phản kháng (kW)
    "Voltage",                # Điện áp lưới (V)
    "Sub_metering_1",         # Bếp: máy rửa bát, lò vi sóng (Wh)
    "Sub_metering_2",         # Phòng giặt: máy giặt, sấy, tủ lạnh (Wh)
    "Sub_metering_3",         # Bình nước nóng, điều hòa nhiệt độ (Wh)
    "Sub_metering_remainder", # Năng lượng tiêu thụ khác ngoài 3 phân hệ đo (Wh)
]

# Các cột đặc trưng phân loại / thời gian
FEATURE_COLS_CATEGORICAL = [
    "hour",
    "day_of_week",
    "is_weekend",
    "month",
]

# Cột gây rò rỉ dữ liệu (Data Leakage):
# Global_intensity là cường độ dòng điện (A). Theo định luật vật lý: P ≈ V * I * cos(phi) / 1000.
# Global_intensity có tương quan > 0.999 với Global_active_power, khiến mô hình học thuộc
# công thức đo đếm tức thời thay vì học quy luật phụ tải -> LOẠI KHỎI ĐẶC TRƯNG.
LEAKY_COLS: list[str] = ["Global_intensity"]

# Loại bỏ nhãn mục tiêu khỏi các tác vụ tương ứng
CLS_EXCLUDE_COLS = [TARGET_REG]
REG_EXCLUDE_COLS = [TARGET_CLS]

# Ngưỡng vật lý kiểm tra tính hợp lý (Data Sanity Checks)
VOLTAGE_RANGE = (200.0, 260.0)  # Điện áp sinh hoạt tiêu chuẩn Châu Âu quanh 230V
POWER_MIN = 0.0

# --- Chia dữ liệu và kiểm định -----------------------------------------------------------------
SPLIT_MODE = "time"       # Chia theo thứ tự thời gian (tránh rò rỉ tương quan chuỗi thời gian)
TEST_FRACTION = 0.2       # 20% test (giai đoạn sau cùng)
TRAIN_RATIO = 1.0 - TEST_FRACTION  # = 0.8 — 80% train (các năm/tháng đầu)
CV_FOLDS = 3              # K-Fold kiểm định chéo trên tập huấn luyện (3 để chạy nhanh hơn trên 2M dòng)
# Giới hạn số dòng train đưa vào GridSearchCV (lấy mẫu ngẫu nhiên có cố định seed để tái lập)
# Dữ liệu gốc ~1.6M dòng train → KNN + 5-fold rất chậm; 50_000 đủ đại diện thống kê
MAX_TRAIN_ROWS = 20_000

# --- Tiền xử lý dữ liệu ------------------------------------------------------------------------
IQR_K = 1.5               # Ngưỡng phát hiện ngoại lai theo IQR
PCA_VARIANCE = 0.95       # Phương sai tích lũy tối thiểu khi giảm chiều PCA

# --- Phân cụm hồ sơ phụ tải ngày ---------------------------------------------------------------
KMEANS_K_MIN = 2
KMEANS_K_MAX = 8
N_KMEANS_INIT = 10
# Số cụm tối ưu chọn sau phân tích Elbow/Silhouette (cập nhật sau T008)
N_CLUSTERS = 3
# Số chiều giảm xuống sau PCA (cập nhật sau T006, chọn k sao cho PCA_VARIANCE >= 0.95)
N_COMPONENTS = 4

# --- Luật kết hợp (Apriori / FP-Growth) ---------------------------------------------------------
MIN_SUPPORT = 0.05
MIN_CONFIDENCE = 0.6
MIN_LIFT = 1.0
HOUR_BIN_EDGES = (0, 6, 12, 18, 24)  # 4 khung giờ: đêm, sáng, chiều, tối
DISCRETIZE_LEVELS = ("thap", "trung_binh", "cao")

# --- Mô hình học máy và lưới siêu tham số ------------------------------------------------------
LOGREG_MAX_ITER = 1000
CLASSIFIER_GRID = {
    "decision_tree": {"max_depth": [3, 5, 7, None]},
    # KNN chạy trên mẫu MAX_TRAIN_ROWS=20_000 → chấp nhận được về CPU
    "knn": {"n_neighbors": [3, 5, 7, 11]},
    "logistic_regression": {"C": [0.1, 1.0, 10.0]},
}
REGRESSOR_GRID = {
    "decision_tree": {"max_depth": [3, 5, 7, 10, None]},
    "linear_regression": {},
}

# Độ đo chính
PRIMARY_METRIC_CLS = "f1_macro"
PRIMARY_METRIC_REG = "rmse"
OUTLIER_POLICY = "flag"   # Đánh dấu ngoại lai, không tùy tiện xóa phụ tải đột biến thật
SAMPLING = "none"

# Đặc trưng trễ (Lag features) dự báo chuỗi thời gian
LAG_STEPS = [1, 2, 4, 96]  # 1 bước (15p), 2 bước (30p), 1 giờ (4 bước), 1 ngày trước (96 bước)

# --- Bắt buộc đầu ra ---------------------------------------------------------------------------
MIN_FIGURES = 8
MIN_FIGURE_TYPES = 4
MIN_RULES_DISCUSSED = 5
CLEAN_DATA_NAME = "household_power_clean.csv"

# --- Tên tệp kết quả dạng bảng (results/tables/) -----------------------------------------------
TBL_QUALITY_BEFORE = "b_01_chat_luong_truoc.csv"
TBL_QUALITY_AFTER = "b_02_chat_luong_sau.csv"
TBL_LEAKAGE = "b_03_kiem_ro_ri.csv"
TBL_CLS_CV = "e_01_phan_lop_cv.csv"
TBL_REG_CV = "e_02_hoi_quy_cv.csv"
TBL_CLS_TUNE = "e_03_chinh_tham_so.csv"
TBL_CLS_TEST = "g_01_phan_lop_tung_lop.csv"
TBL_CLS_CONFUSIONS = "g_02_cap_nham_lan.csv"
TBL_REG_TEST = "g_03_hoi_quy_kiem_tra.csv"
TBL_REG_LAGS = "g_04_hoi_quy_kem_dac_trung_tre.csv"
TBL_CLS_ERR_HOUR = "g_05_loi_phan_lop_theo_gio.csv"
TBL_CLS_ERR_DAYTYPE = "g_06_loi_phan_lop_theo_loai_ngay.csv"
TBL_IMP_CLS = "g_07_do_quan_trong_phan_lop.csv"
TBL_IMP_REG = "g_08_do_quan_trong_hoi_quy.csv"
