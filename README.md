# ETL Pipeline Project ⚙️

Proyek ini adalah implementasi alur kerja **ETL (Extract, Transform, Load)** otomatis untuk mengolah data mentah menjadi data siap pakai. Pipeline ini dirancang untuk memastikan kualitas data sebelum masuk ke tahap analisis mendalam atau pemodelan Machine Learning.

## 🔄 Alur Kerja (Workflow)
1. **Extract**: Mengambil data dari berbagai sumber (CSV, SQL, atau API).
2. **Transform**: 
   - Membersihkan nilai yang hilang (missing values).
   - Menghapus data duplikat.
   - Normalisasi dan standarisasi fitur (Scaling).
   - Penanganan outliers agar tidak mengganggu proses clustering.
3. **Load**: Menyimpan data yang sudah bersih ke dalam format baru (CSV/Parquet) atau database untuk kebutuhan selanjutnya.

## 🛠️ Tech Stack
- **Language**: Python
- **Libraries**: Pandas, NumPy (Data Manipulation), Scikit-Learn (Preprocessing)
- **Visualization**: Matplotlib/Seaborn (untuk pengecekan distribusi data)

## 📂 Struktur Proyek
- `data/`: Folder berisi dataset mentah (raw) dan hasil olahan (processed).
- `scripts/`: Berisi file Python utama untuk setiap tahap ETL.
- `notebooks/`: Dokumentasi eksplorasi data (EDA) dan pengujian pipeline.

## 🚀 Cara Menjalankan
1. Pastikan Python sudah terinstal.
2. Buat Virtual Environment (Opsional tapi disarankan):
    ```bash
    python -m venv venv
    source venv/bin/activate  # Untuk Windows: venv\Scripts\activate

3. Instal dependensi:
   ```bash
   pip install -r requirements.txt

4. Jalankan Pipeline::
    ```bash
    python main.py


## 🧪 Testing
Proyek ini dilengkapi dengan unit testing. Untuk menjalankan tes dan melihat laporan coverage:
### Menjalankan unit test pada folder tests
    python -m pytest tests

### Menjalankan test coverage pada folder tests
    coverage run -m pytest tests
