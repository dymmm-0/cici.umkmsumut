from flask import Flask, render_template, request
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB

# ===================== KONFIGURASI =====================
K_VALUE = 5
TEST_SIZE = 0.2
RANDOM_STATE = 42
MIN_ROWS = 10

# PErtanyaan yang ada di Kuisoner
FEATURE_COLS = [
    "Bagaimana Pendapat Saudara Tentang Kesesuaian Persyaratan Pelayanan dengan Jenis Pelayanannya",
    "Bagaimana Pemahaman Saudara Tentang Kemudahan Prosedur Pelayanan di Unit ini?",
    "Bagaimana Pendapat Saudara Tentang Kewajaran Biaya/Tarif dalam Pelayanan?",
    "Bagaimana Pendapat Saudara Tentang Kesesuaian Produk Pelayanan yang Tercantum dalam Standar Pelayanan dengan hasil yang Diberikan?",
    "Bagaimana Pendapat Saudara Tentang Kompetensi/Kemampuan Petugas Dalam Pelayanan",
    "Bagaimana Pendapat Saudara Perilaku Petugas Dalam Pelayanan Terkait Kesopanan dan Keramahan?",
    "Bagaimana Pendapat Saudara Tentang Kualitas Sarana dan Prasarana",
    "Bagaimana Pendapat Saudara Tentang Penanganan Pengaduan Pengguna Layanan",
    "Bagaimana Pendapat Saudara Tetang Kecepatan Waktu  dalam Memberikan pelayanan?"
]

# Skala LIKERT 1–5 
RESPONSE_MAPPING_1_5 = {
    # Kesesuaian
    "Sangat Sesuai": 5, "Sesuai": 4, "Cukup Sesuai": 3, "Kurang Sesuai": 2, "Tidak Sesuai": 1,

    # Kemudahan
    "Sangat Mudah": 5, "Mudah": 4, "Cukup Mudah": 3, "Kurang Mudah": 2, "Tidak Mudah": 1,

    # Kewajaran
    "Sangat Wajar": 5, "Wajar": 4, "Cukup Wajar": 3, "Kurang Wajar": 2, "Tidak Wajar": 1,

    # Biaya/Tarif
    "Gratis": 5, "Murah": 4, "Cukup Mahal": 3, "Mahal": 2, "Sangat Mahal": 1,

    # Produk pelayanan
    "Sangat Baik": 5, "Baik": 4, "Cukup": 3, "Kurang": 2, "Buruk": 1,

    # Kompetensi
    "Sangat Kompeten": 5, "Kompeten": 4, "Cukup Kompeten": 3, "Kurang Kompeten": 2, "Tidak Kompeten": 1,

    # Perilaku petugas
    "Sangat Sopan Dan Ramah": 5, "Sopan Dan Ramah": 4, "Cukup Sopan Dan Ramah": 3,
    "Kurang Sopan Dan Ramah": 2, "Tidak Sopan Dan Ramah": 1,

    # Penanganan pengaduan
    "Dikelola Dengan Baik": 5, "Dikelola Baik": 5, "Dikelola": 4,
    "Berfungsi Kurang Maksimal": 3, "Ada Tetapi Tidak Berfungsi": 2, "Tidak Ada": 1,

    # Kecepatan
    "Sangat Cepat": 5, "Cepat": 4, "Cukup Cepat": 3, "Kurang Cepat": 2, "Tidak Cepat": 1,

    # Kepuasan langsung (kalau muncul)
    "Sangat Puas": 5, "Puas": 4, "Cukup Puas": 3, "Tidak Puas": 2, "Sangat Tidak Puas": 1,
}

# Membaca file Excel/CSV
def read_file(file_storage) -> pd.DataFrame:
    filename = (file_storage.filename or "").lower()
    if filename.endswith(".csv"):
        return pd.read_csv(file_storage)
    if filename.endswith(".xlsx") or filename.endswith(".xls"):
        return pd.read_excel(file_storage)
    raise ValueError("Format file harus CSV atau XLSX.")


    # NOTE: pakai title-case agar mapping konsisten
def normalize_text_series(s: pd.Series) -> pd.Series:
    return (
        s.astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.replace("’", "'", regex=False)
        .str.title()
    )


def label_from_avg_1_5(avg_scores: pd.Series) -> pd.Series:
    return pd.cut(
        avg_scores,
        bins=[0, 2.33, 3.66, 5.00],
        labels=["Kurang", "Cukup", "Baik"],
        include_lowest=True
    ).astype(str)


def safe_split(X, y, test_size, random_state):
    y_series = pd.Series(y)
    vc = y_series.value_counts()
    use_stratify = (len(vc) >= 2) and (vc.min() >= 2)

    if use_stratify:
        return train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
    return train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )


def preprocess_data(df: pd.DataFrame):
    log = []

    log.append("=== TAHAP 1: DATA CLEANING ===")
    original_count = len(df)

    missing_cols = [c for c in FEATURE_COLS if c not in df.columns]
    if missing_cols:
        preview = missing_cols[:3]
        raise ValueError(
            f"Kolom tidak ditemukan: {preview} ... "
            f"(pastikan header Excel sama persis dengan FEATURE_COLS di app.py)"
        )

    df_feat = df[FEATURE_COLS].copy()
    df_feat = df_feat.dropna()
    clean_count = len(df_feat)

    if clean_count < MIN_ROWS:
        raise ValueError(f"Data valid terlalu sedikit (minimal {MIN_ROWS} baris). Periksa isi file Excel.")

    log.append("\n=== TAHAP 2: DATA TRANSFORMATION ===")

    df_num = df_feat.copy()
    unmapped_examples = {}

    for col in FEATURE_COLS:
        norm = normalize_text_series(df_num[col])
        mapped = norm.map(RESPONSE_MAPPING_1_5)

        mask_unmapped = mapped.isna()
        if mask_unmapped.any():
            unmapped_examples[col] = norm[mask_unmapped].dropna().unique().tolist()[:5]

        df_num[col] = mapped

    before_drop = len(df_num)
    df_num = df_num.dropna()
    after_transform = len(df_num)

    if after_transform < MIN_ROWS:
        msg = (
            f"Data valid terlalu sedikit setelah transformasi ({after_transform}). "
            "Kemungkinan ada jawaban yang belum ada mapping.\n"
        )
        if unmapped_examples:
            msg += "\nContoh nilai yang belum termapping (per kolom):\n"
            for k, v in list(unmapped_examples.items())[:3]:
                msg += f"- {k[:45]}... : {v}\n"
        raise ValueError(msg)

    log.append("\n=== TAHAP 3: DATA NORMALIZATION ===")
    X_raw = df_num.values.astype(float)
    scaler = MinMaxScaler()
    X_norm = scaler.fit_transform(X_raw)

    log.append("\n=== TAHAP 4: LABELING/CLASSIFICATION ===")
    avg_scores = df_num.mean(axis=1)
    y_all = label_from_avg_1_5(avg_scores)

    log.append("\n=== TAHAP 5: DATA DIVISION ===")
    X_train, X_test, y_train, y_test = safe_split(X_norm, y_all, TEST_SIZE, RANDOM_STATE)
    return {
        "original_count": original_count,
        "valid_count": after_transform,
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "X_norm": X_norm,
        "y_all": y_all,
        "preprocessing_log": log,
    }

def stable_labels(y_all):
    return ["Kurang", "Cukup", "Baik"]


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", has_result=False)


@app.route("/process", methods=["POST"])
def process():
    f = request.files.get("datafile")
    if not f or f.filename == "":
        return render_template("index.html", has_result=False, error="File belum dipilih.")

    try:
        df = read_file(f)
        prep = preprocess_data(df)

        X_train = prep["X_train"]
        X_test = prep["X_test"]
        y_train = prep["y_train"]
        y_test = prep["y_test"]
        X_norm = prep["X_norm"]
        y_all = prep["y_all"]

        # ===== KNN =====
        model = KNeighborsClassifier(n_neighbors=K_VALUE)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # ===== EVALUASI =====
        labels_sorted = stable_labels(y_all)

        acc = accuracy_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred, labels=labels_sorted)
        report = classification_report(y_test, y_pred, labels=labels_sorted, output_dict=True, zero_division=0)
        
        # diagram pie chart
        precision = round(report["macro avg"]["precision"] * 100, 2)
        recall =  round(report["macro avg"]["recall"] * 100, 2)
        f1_score = round(report["macro avg"]["f1-score"] * 100, 2)

        # Rekap prediksi seluruh data
        all_pred = model.predict(X_norm)
        pred_counts = pd.Series(all_pred).value_counts().to_dict()
        pred_counts = {lab: int(pred_counts.get(lab, 0)) for lab in labels_sorted}

        # render balik ke index (hasil muncul di "Keterangan Sistem")
        return render_template(
            "index.html",
            has_result=True,
            error=None,
            filename=f.filename,
            original_count=prep["original_count"],
            valid_count=prep["valid_count"],
            preprocessing_log=prep["preprocessing_log"],
            k_value=K_VALUE,
            train_size=len(X_train),
            test_size=len(X_test),
            acc=round(acc * 100, 2),
            precision=round(precision, 2),
            recall=round(recall, 2),
            f1_score=round(f1_score, 2),
            labels=labels_sorted,
            cm=cm.tolist(),
            pred_counts=pred_counts,
            report=report,
            feature_cols=FEATURE_COLS,
        )

    except Exception as e:

        return render_template("index.html", has_result=False, error=str(e))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
