import pandas as pd

from utils.extract import scrape_collection_data
from utils.transform import transform
from utils.load import store_to_csv, store_to_spreadsheet, store_to_postgre, create_database

def main():
    """Fungsi utama menjalankan ETL: Scraping → Transform → Load"""
    
    url = 'https://fashion-studio.dicoding.dev'
    
    # -----------------------------
    # Extract
    # -----------------------------
    print("[INFO] Memulai proses ekstraksi data...")
    collection_data = scrape_collection_data(url)
    
    if not collection_data:
        print("[WARNING] Tidak ada data yang ditemukan. Proses dihentikan.")
        return
    
    print(f"[INFO] Berhasil mengambil data ({len(collection_data)} item).")
    
    # -----------------------------
    # Transform
    # -----------------------------
    print("[INFO] Memulai proses transformasi data...")
    df = transform(collection_data)
    print(f"[INFO] Data setelah transformasi: {df.shape[0]} baris x {df.shape[1]} kolom")
    
    # Cek tipe data
    print(df.info())
    
    # -----------------------------
    # Load
    # -----------------------------
    # Store to CSV
    store_to_csv(df, filepath='products.csv')
    
    # Store to Google Sheets
    spreadsheet_id = '1UbjXeVfjk_xmn1N13pAgBlWNz7tFcf6A6a7HlSs1LhQ'
    worksheet_name='Sheet1'
    credentials_json='google-sheets-api.json'
    store_to_spreadsheet(df, spreadsheet_id, worksheet_name, credentials_json)
    
    # Store to PostgreSQL
    db_name = 'productsdb'
    create_database(db_name)
    db_url = 'postgresql+psycopg2://developer:supersecretpassword@localhost:5432/productsdb'
    store_to_postgre(df, db_url)
    
    print("[INFO] Proses ETL selesai!")

if __name__ == "__main__":
    main()