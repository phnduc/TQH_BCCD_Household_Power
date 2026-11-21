"""Kịch bản thực thi toàn bộ luồng phân tích và dự báo phụ tải (chủ: Đức).

Chạy toàn bộ pipeline từ tải dữ liệu, tiền xử lý, huấn luyện mô hình phân lớp & hồi quy,
đánh giá hiệu năng và xuất kết quả ra thư mục results/tables/.
"""
from __future__ import annotations

import pandas as pd
from sklearn.tree import DecisionTreeClassifier

from src import config, data_prep, evaluate, models


def _save(df: pd.DataFrame, name: str) -> None:
    config.TABLE_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(config.TABLE_DIR / name, index=False)


def stage_b() -> pd.DataFrame:
    """Giai đoạn làm sạch và kiểm tra chất lượng dữ liệu."""
    print("-> Bắt đầu Giai đoạn B: Tiền xử lý dữ liệu...")
    raw = data_prep.load_raw()
    _save(data_prep.quality_report(raw), config.TBL_QUALITY_BEFORE)
    clean = data_prep.clean(raw)
    _save(data_prep.quality_report(clean), config.TBL_QUALITY_AFTER)
    data_prep.save_clean(clean)
    _save(_leakage_table(clean), config.TBL_LEAKAGE)
    print("   Đã hoàn thành Giai đoạn B và lưu dữ liệu sạch.")
    return clean


def _leakage_table(df: pd.DataFrame) -> pd.DataFrame:
    """Bằng chứng kiểm tra rò rỉ dữ liệu giữa Global_intensity và Global_active_power."""
    train, test = data_prep.time_split(df)
    corr = df[config.TARGET_REG].corr(df["Global_intensity"]) if "Global_intensity" in df.columns else 0.0
    tree = DecisionTreeClassifier(random_state=config.SEED).fit(train[[config.TARGET_REG]], train[config.TARGET_CLS])
    acc = (tree.predict(test[[config.TARGET_REG]]) == test[config.TARGET_CLS]).mean()
    return pd.DataFrame([
        {
            "kiem_tra": "tuong_quan_pearson(Global_active_power, Global_intensity)",
            "gia_tri": corr,
            "ket_luan": "Global_intensity rò rỉ trực tiếp công suất (P ≈ V*I): LOẠI KHỎI ĐẶC TRƯNG",
        },
        {
            "kiem_tra": "accuracy_cay_chi_dung_Global_active_power_doan_Load_Level",
            "gia_tri": acc,
            "ket_luan": "Load_Level tạo từ tam phân vị của chuỗi công suất",
        },
    ])


def _sample_train(train: pd.DataFrame) -> pd.DataFrame:
    """Lấy mẫu tập train để GridSearchCV chạy nhanh hơn.

    Với ~1.6M dòng, GridSearchCV + KNN + 3-fold rất chậm.
    Lấy mẫu phân tầng (stratified) theo Load_Level, tối đa MAX_TRAIN_ROWS dòng.
    """
    if len(train) <= config.MAX_TRAIN_ROWS:
        return train
    print(f"   [SAMPLE] Train {len(train):,} dong -> lay mau {config.MAX_TRAIN_ROWS:,} dong "
          f"(stratified, seed={config.SEED})")
    return train.groupby(config.TARGET_CLS, group_keys=False).apply(
        lambda g: g.sample(
            n=max(1, int(config.MAX_TRAIN_ROWS * len(g) / len(train))),
            random_state=config.SEED,
        )
    )


def stage_models(clean: pd.DataFrame) -> None:
    """Giai đoạn huấn luyện và đánh giá các mô hình phân lớp & hồi quy."""
    print("-> Bắt đầu Giai đoạn E & G: Huấn luyện và đánh giá mô hình...")
    train_full, test = data_prep.time_split(clean)
    train = _sample_train(train_full)
    labels = config.LOAD_CLASSES

    # 1. Phân lớp mức phụ tải
    xc_tr, xc_te = data_prep.make_features(train, test, "cls")
    clfs = models.train_classifiers(xc_tr, train[config.TARGET_CLS])
    cv_rows, test_tables, confusions = [], [], []
    for name, m in clfs.items():
        print(f"   [CLS] {name}: best_params={m.best_params_}, f1_macro={m.best_score_:.4f}")
        cv_rows.append({"mo_hinh": name, "tham_so_tot_nhat": str(m.best_params_), "f1_macro_cv": m.best_score_})
        cv_rows.append({"mo_hinh": name, "tham_so_tot_nhat": str(m.best_params_), "f1_macro_cv": m.best_score_})
        pred = m.predict(xc_te)
        t = evaluate.classification_report_table(test[config.TARGET_CLS], pred, labels)
        test_tables.append(t.assign(mo_hinh=name))
        confusions.append(evaluate.top_confusions(test[config.TARGET_CLS], pred, labels).assign(mo_hinh=name))

    best = max(clfs, key=lambda n: clfs[n].best_score_)
    best_pred = clfs[best].predict(xc_te)
    _save(evaluate.error_by_group(test[config.TARGET_CLS], best_pred, test["hour"]), config.TBL_CLS_ERR_HOUR)
    _save(evaluate.error_by_group(test[config.TARGET_CLS], best_pred, test["day_of_week"]), config.TBL_CLS_ERR_DAYTYPE)
    _save(evaluate.feature_importance_table(clfs["decision_tree"], list(xc_tr.columns)), config.TBL_IMP_CLS)
    _save(pd.DataFrame(cv_rows), config.TBL_CLS_CV)
    _save(pd.concat(test_tables, ignore_index=True), config.TBL_CLS_TEST)
    _save(pd.concat(confusions, ignore_index=True), config.TBL_CLS_CONFUSIONS)

    # 2. Hồi quy dự báo công suất
    print("   [REG] Huấn luyện mô hình hồi quy...")
    xr_tr, xr_te = data_prep.make_features(train, test, "reg")
    regs = models.train_regressors(xr_tr, train[config.TARGET_REG])
    rows, test_rows = [], []
    for name, m in regs.items():
        print(f"   [REG] {name}: rmse_cv={-m.best_score_:.4f}")
        rows.append({"mo_hinh": name, "tham_so_tot_nhat": str(m.best_params_), "rmse_cv": -m.best_score_})
        rows.append({"mo_hinh": name, "tham_so_tot_nhat": str(m.best_params_), "rmse_cv": -m.best_score_})
        test_rows.append({"mo_hinh": name, **evaluate.regression_report(test[config.TARGET_REG], m.predict(xr_te))})
    _save(pd.DataFrame(rows), config.TBL_REG_CV)
    _save(pd.DataFrame(test_rows), config.TBL_REG_TEST)
    _save(evaluate.feature_importance_table(regs["decision_tree"], list(xr_tr.columns)), config.TBL_IMP_REG)

    # 3. Hồi quy dự báo có thêm đặc trưng trễ (Lag features)
    print("   [LAG] Thêm lag features và huấn luyện lại hồi quy...")
    lagged = data_prep.add_lag_features(clean)
    l_tr_full, l_te = data_prep.time_split(lagged)
    l_tr = _sample_train(l_tr_full)
    xl_tr, xl_te = data_prep.make_features(l_tr, l_te, "reg")
    lags = data_prep.lag_feature_names()
    xl_tr = xl_tr.join(l_tr[lags])
    xl_te = xl_te.join(l_te[lags])
    regs_lags = models.train_regressors(xl_tr, l_tr[config.TARGET_REG])
    lag_rows = []
    for name, m in regs_lags.items():
        lag_rows.append({
            "mo_hinh": f"{name}_with_lags",
            "tham_so_tot_nhat": str(m.best_params_),
            "rmse_cv": -m.best_score_,
            **evaluate.regression_report(l_te[config.TARGET_REG], m.predict(xl_te))
        })
    _save(pd.DataFrame(lag_rows), config.TBL_REG_LAGS)
    print("   Đã hoàn thành huấn luyện và lưu toàn bộ bảng kết quả vào results/tables/.")


def main() -> None:
    clean = stage_b()
    stage_models(clean)
    print("=== CHẠY TOÀN BỘ QUY TRÌNH THÀNH CÔNG ===")


if __name__ == "__main__":
    main()
