# ETL Pipeline Project ⚙️

Proyek ini adalah implementasi sederhana dari alur kerja **ETL (Extract, Transform, Load)** menggunakan Python. Proyek ini mendemonstrasikan cara mengambil data dari file CSV, melakukan pembersihan data, dan menyiapkannya untuk analisis lebih lanjut.

## 📁 Struktur Proyek
- `main.py`: Entry point utama untuk menjalankan seluruh pipeline ETL.
- `utils/`: Folder berisi modul pembantu untuk logika transformasi data.
- `tests/`: Berisi unit testing untuk memastikan setiap fungsi berjalan dengan benar.
- `products.csv`: Dataset sampel yang dihasilkan dari proses ETL ini.

## 🛠️ Tech Stack
- **Language**: Python 3
- **Libraries**: Pandas (Data Manipulation), Pytest (Testing)



## 🔐 Persiapan Kredensial (Setup) untuk upload ke GSheets

Proyek ini memerlukan akses ke **Google Sheets API**. Karena alasan keamanan, file kredensial tidak disertakan dalam repositori ini.

1. Buat project di [Google Cloud Console](https://console.cloud.google.com/).
2. Aktifkan **Google Sheets API** dan **Google Drive API**.
3. Buat **Service Account** dan unduh kunci (key) dalam format `.json`.
4. Letakkan di root folder proyek ini.
5. Pastikan Email Service Account tersebut sudah di-"Share" ke Google Sheets yang ingin kamu akses (sebagai Editor).

## 🔐 Persiapan Environment (.env)

Buat file bernama `.env` di folder utama dan isi dengan konfigurasi berikut:

```text
GOOGLE_SHEETS_CREDENTIALS=[nama file key .json]
SPREADSHEET_ID=[isi_dengan_id_spreadsheet]
WORKSHEET_NAME=Sheet1 #Atau isi dengan nama worksheet yang diinginkan
```


## 🚀 Cara Menjalankan
1. Clone repositori ini:
   ```bash
   git clone https://github.com/waryuu/ETL-Pipeline-Project.git
   cd ETL-Pipeline-Project

2. Buat Virtual Environment (Opsional tapi disarankan):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Untuk Windows: venv\Scripts\activate

3. Instal dependensi:
   ```bash
   pip install -r requirements.txt

4. Jalankan Pipeline::
    ```bash
    python main.py


## 🧪 Testing & Quality Assurance

Proyek ini menggunakan **Pytest** untuk unit testing dan **Coverage.py** untuk mengukur sejauh mana kode telah diuji.

### Menjalankan Unit Test
Gunakan perintah berikut untuk menjalankan seluruh test case di folder `tests/`:
    ```bash
    python -m pytest tests

### Menjalankan Test Coverage
1. Untuk melihat laporan cakupan pengujian (test coverage):
    ```bash
    coverage run -m pytest tests

2. Jalankan pengujian dengan coverage:
    ```bash
    coverage report

3. (Opsional) Buat laporan dalam bentuk HTML yang interaktif:
    ```bash
    coverage html
    
Hasilnya dapat dilihat di folder htmlcov/index.html.