# Truy vết hình và bảng của DA
| Số hình / bảng | Tệp | Hàm / Notebook | Mã task | Nhận xét rút ra |
|---|---|---|---|---|
| Bảng e_01 | `results/tables/e_01_phan_lop_cv.csv` | `train_classifiers` | T007 | Decision Tree đạt F1 macro cao nhất trên tập huấn luyện |
| Bảng g_01 | `results/tables/g_01_phan_lop_tung_lop.csv` | `stage_models` | T007 | Lớp Low_Load có F1 cao nhất, lớp Normal_Load bị nhầm lẫn nhiều nhất |
| Bảng g_03 | `results/tables/g_03_hoi_quy_kiem_tra.csv` | `stage_models` | T007 | Decision Tree Regressor đạt RMSE 0.38 kW trên tập test |
| Bảng g_04 | `results/tables/g_04_hoi_quy_kem_dac_trung_tre.csv` | `stage_models` | T015 | Bổ sung đặc trưng trễ (lags) giúp giảm RMSE xuống còn 0.22 kW |
