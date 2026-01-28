# 📊 UMKM KNN Web Application

Aplikasi web berbasis Flask untuk klasifikasi dan analisis kepuasan pelayanan UMKM menggunakan algoritma **K-Nearest Neighbors (KNN)** dengan visualisasi interaktif.

## 🎯 Fitur Utama

- **Upload Data**: Mendukung format CSV dan Excel (.xlsx, .xls)
- **Preprocessing Otomatis**: Cleaning, transformasi, dan normalisasi data
- **Klasifikasi KNN**: Menggunakan scikit-learn dengan K=5
- **Evaluasi Model**: Accuracy, Precision, Recall, F1-Score
- **Visualisasi**: 
  - Confusion Matrix interaktif
  - Pie Chart distribusi prediksi
  - Bar Chart metrik evaluasi
- **Responsive Design**: Tampilan modern dengan animasi

## 📋 Kategori Klasifikasi

Sistem mengklasifikasikan kepuasan pelayanan ke dalam 3 kategori berdasarkan rata-rata skor (skala Likert 1-5):

- **Baik**: Skor rata-rata 3.67 - 5.00
- **Cukup**: Skor rata-rata 2.34 - 3.66
- **Kurang**: Skor rata-rata 1.00 - 2.33

## 🔧 Teknologi

- **Backend**: Flask (Python)
- **Machine Learning**: scikit-learn
- **Data Processing**: pandas, numpy
- **Frontend**: HTML5, CSS3, JavaScript
- **Visualisasi**: Chart.js

## 📦 Instalasi

### Prerequisites
- Python 3.7+
- pip

### Langkah Instalasi

1. Clone repository
```bash
git clone https://github.com/dymmm-0/umkm-knn-web.git
cd umkm-knn-web
```

2. Buat virtual environment (opsional tapi direkomendasikan)
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Jalankan aplikasi
```bash
python app.py
```

5. Buka browser dan akses
```
http://127.0.0.1:5001
```

## 📊 Format Data Input

File Excel/CSV harus memiliki kolom-kolom berikut (sesuai pertanyaan kuesioner):

1. Bagaimana Pendapat Saudara Tentang Kesesuaian Persyaratan Pelayanan dengan Jenis Pelayanannya
2. Bagaimana Pemahaman Saudara Tentang Kemudahan Prosedur Pelayanan di Unit ini?
3. Bagaimana Pendapat Saudara Tentang Kewajaran Biaya/Tarif dalam Pelayanan?
4. Bagaimana Pendapat Saudara Tentang Kesesuaian Produk Pelayanan yang Tercantum dalam Standar Pelayanan dengan hasil yang Diberikan?
5. Bagaimana Pendapat Saudara Tentang Kompetensi/Kemampuan Petugas Dalam Pelayanan
6. Bagaimana Pendapat Saudara Perilaku Petugas Dalam Pelayanan Terkait Kesopanan dan Keramahan?
7. Bagaimana Pendapat Saudara Tentang Kualitas Sarana dan Prasarana
8. Bagaimana Pendapat Saudara Tentang Penanganan Pengaduan Pengguna Layanan
9. Bagaimana Pendapat Saudara Tetang Kecepatan Waktu  dalam Memberikan pelayanan?

### Contoh Nilai yang Valid

Setiap kolom harus berisi jawaban dalam skala Likert, contoh:
- **Kesesuaian**: Sangat Sesuai, Sesuai, Cukup Sesuai, Kurang Sesuai, Tidak Sesuai
- **Kemudahan**: Sangat Mudah, Mudah, Cukup Mudah, Kurang Mudah, Tidak Mudah
- **Kewajaran**: Sangat Wajar, Wajar, Cukup Wajar, Kurang Wajar, Tidak Wajar
- Dan seterusnya...

## 🚀 Cara Penggunaan

1. Siapkan file data dalam format Excel (.xlsx) atau CSV
2. Pastikan file memiliki minimal 10 baris data valid
3. Klik tombol "Choose File" dan pilih file Anda
4. Klik "Upload & Proses"
5. Tunggu proses selesai dan lihat hasil analisis

## 📈 Output Sistem

Setelah proses selesai, sistem akan menampilkan:

- **Informasi Dataset**: Jumlah data original dan valid
- **Log Preprocessing**: Detail tahapan pemrosesan data
- **Konfigurasi Model**: Nilai K, ukuran data training/testing
- **Metrik Evaluasi**: Accuracy, Precision, Recall, F1-Score
- **Confusion Matrix**: Visualisasi performa klasifikasi
- **Distribusi Prediksi**: Pie chart hasil klasifikasi keseluruhan data
- **Classification Report**: Detail metrik per kategori

## ⚙️ Konfigurasi

Anda dapat mengubah parameter di file `app.py`:

```python
K_VALUE = 5              # Jumlah tetangga terdekat
TEST_SIZE = 0.2          # Proporsi data testing (20%)
RANDOM_STATE = 42        # Seed untuk reproducibility
MIN_ROWS = 10            # Minimal baris data valid
```

## 🐛 Troubleshooting

### Error: "Kolom tidak ditemukan"
- Pastikan nama kolom di Excel sama persis dengan yang ada di `FEATURE_COLS`
- Periksa tidak ada spasi berlebih atau karakter khusus

### Error: "Data valid terlalu sedikit"
- Pastikan file memiliki minimal 10 baris data
- Periksa tidak ada baris kosong atau data yang tidak valid

### Error: "Nilai yang belum termapping"
- Pastikan semua jawaban menggunakan format yang sudah didefinisikan
- Cek `RESPONSE_MAPPING_1_5` di `app.py` untuk daftar nilai valid

## 📝 Lisensi

MIT License

## 👤 Author

**dymmm-0**
- GitHub: [@dymmm-0](https://github.com/dymmm-0)

## 🤝 Kontribusi

Kontribusi, issues, dan feature requests sangat diterima!

---

⭐ Jangan lupa beri star jika project ini membantu Anda!
