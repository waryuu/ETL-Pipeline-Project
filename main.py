import pandas as pd
import os
from utils.extract import scrape_collection_data
from utils.transform import transform
from utils.load import store_to_csv, store_to_spreadsheet, store_to_postgre, create_database
from dotenv import load_dotenv




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

    load_dotenv()
    # Ambil data dari .env
    credentials_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
    spreadsheet_id = os.getenv('SPREADSHEET_ID')
    worksheet_name = os.getenv('WORKSHEET_NAME')

    store_to_spreadsheet(df, spreadsheet_id, worksheet_name, credentials_json)
    
    # Store to PostgreSQL
    db_name = 'productsdb'
    create_database(db_name)
    db_url = 'postgresql+psycopg2://developer:supersecretpassword@localhost:5432/productsdb'
    store_to_postgre(df, db_url)
    
    print("[INFO] Proses ETL selesai!")

if __name__ == "__main__":
    main()