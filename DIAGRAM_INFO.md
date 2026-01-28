# Dokumentasi Diagram Visualisasi

## Perubahan yang Dibuat

### 1. File `app.py`
Ditambahkan kode untuk generate 3 jenis diagram:

#### a. Pie Chart - Distribusi Hasil Klasifikasi
- Menampilkan persentase distribusi kelas (Kurang, Cukup, Baik)
- Menggunakan warna: Merah (Kurang), Orange (Cukup), Hijau (Baik)
- Format: Pie chart dengan label persentase

#### b. Bar Chart - Metrik Evaluasi Model
- Menampilkan 4 metrik: Precision, Recall, F1-Score, Accuracy
- Setiap bar memiliki warna berbeda untuk kemudahan membaca
- Nilai persentase ditampilkan di atas setiap bar

#### c. Heatmap - Confusion Matrix
- Visualisasi confusion matrix dalam bentuk heatmap
- Warna hijau dengan intensitas berbeda sesuai nilai
- Angka ditampilkan di setiap cell untuk detail

### 2. File `index.html`
Ditambahkan section untuk menampilkan 3 diagram di bagian "Keterangan Sistem" setelah tabel hasil klasifikasi.

### 3. File `requirements.txt`
Ditambahkan library `matplotlib==3.8.2` untuk membuat diagram.

## Cara Menggunakan

1. Install dependencies baru:
```bash
pip install -r requirements.txt
```

2. Jalankan aplikasi:
```bash
python app.py
```

3. Upload file Excel/CSV, dan diagram akan otomatis muncul di halaman hasil.

## Teknologi yang Digunakan

- **Matplotlib**: Library untuk membuat diagram
- **Base64 Encoding**: Untuk embed gambar langsung ke HTML tanpa perlu save file
- **Flask**: Framework web untuk render template dengan data diagram
