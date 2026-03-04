import csv
import pandas as pd
import gspread
import psycopg2

from sqlalchemy import create_engine, text
from psycopg2 import sql
from psycopg2.errors import InsufficientPrivilege
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials

# -----------------------------
# Store ke CSV
# -----------------------------
def store_to_csv(data, filepath='products.csv'):
    """
    Menyimpan DataFrame ke file CSV.
    """
    try:
        if data is None or data.empty:
            print("[WARNING] Data kosong, tidak ada yang disimpan ke CSV.")
            return

        data.to_csv(filepath, index=False)
        print(f"[INFO] Data berhasil disimpan di {filepath}")

    except Exception as e:
        print(f"[ERROR] Gagal menyimpan CSV: {e}")
   
# -----------------------------
# Store ke Google Spreadsheet
# -----------------------------
def store_to_spreadsheet(
    data,
    spreadsheet_id,
    worksheet_name,
    credentials_json
):
    """
    Mengupload DataFrame ke Google Sheets.
    """
    try:
        if data is None or data.empty:
            print("[WARNING] Data kosong, tidak ada yang diupload.")
            return

        # Scope akses Google API
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]

        # Autentikasi menggunakan service account
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_json,
            scope
        )

        client = gspread.authorize(creds)

        # Membuka spreadsheet dan worksheet
        sheet = client.open_by_key(spreadsheet_id).worksheet(worksheet_name)

        # Hapus isi lama sebelum upload
        sheet.clear()

        # Upload DataFrame ke worksheet
        set_with_dataframe(sheet, data)

        print(f"[INFO] Data berhasil diupload ke Google Sheets ({worksheet_name})")

    except FileNotFoundError:
        print(f"[ERROR] File credential JSON tidak ditemukan: {credentials_json}")

    except gspread.exceptions.APIError as e:
        print(f"[ERROR] Error API Google Sheets: {e}")

    except Exception as e:
        print(f"[ERROR] Gagal upload ke Google Sheets: {e}")

# -----------------------------
# PostgreSQL - Create Database
# -----------------------------
def create_database(
    db_name,
    user='developer',
    password='supersecretpassword',
    host='localhost',
    port=5432
):
    """
    Membuat database baru jika belum ada.
    """
    try:
        # Koneksi ke database default (postgres)
        with psycopg2.connect(
            dbname='postgres',
            user=user,
            password=password,
            host=host,
            port=port
        ) as conn:

            # Autocommit agar bisa CREATE DATABASE
            conn.autocommit = True

            with conn.cursor() as cur:

                # Cek apakah database sudah ada
                cur.execute(
                    "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s",
                    (db_name,)
                )

                if not cur.fetchone():
                    cur.execute(
                        sql.SQL("CREATE DATABASE {}")
                        .format(sql.Identifier(db_name))
                    )
                    print(f"[INFO] Database '{db_name}' berhasil dibuat.")
                else:
                    print(f"[INFO] Database '{db_name}' sudah ada.")

    except Exception as e:
        print(f"[ERROR] Gagal membuat database: {e}")

# -----------------------------
# Store ke PostgreSQL
# -----------------------------
def store_to_postgre(
    data,
    db_url,
    table_name='producttoscrape',
    required_columns=None
):
    """
    Menyimpan DataFrame ke PostgreSQL.
    """

    if required_columns is None:
        required_columns = [
            'Title', 'Price', 'Rating',
            'Colors', 'Size', 'Gender', 'Timestamp'
        ]

    try:
        if data is None or data.empty:
            print("[WARNING] Data kosong, tidak ada yang disimpan ke database.")
            return

        # Validasi kolom wajib
        missing_cols = [
            col for col in required_columns
            if col not in data.columns
        ]

        if missing_cols:
            raise ValueError(
                f"Kolom berikut tidak ada di DataFrame: {missing_cols}"
            )

        # Membuat koneksi SQLAlchemy
        engine = create_engine(db_url)

        # SQL untuk membuat tabel jika belum ada
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            product_title TEXT NOT NULL,
            price NUMERIC(10,2) NOT NULL,
            ratings NUMERIC(3,2) NOT NULL,
            colors INTEGER NOT NULL,
            size TEXT NOT NULL,
            gender TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL
        )
        """

        # Eksekusi pembuatan tabel
        try:
            with engine.connect() as conn:
                conn.execute(text(create_table_sql))

        except InsufficientPrivilege:
            raise RuntimeError(
                "User database tidak memiliki privilege CREATE TABLE. "
                "Berikan hak akses atau gunakan user lain."
            )

        # Insert data ke tabel
        data.to_sql(
            table_name,
            con=engine,
            if_exists='append',
            index=False
        )

        print(f"[INFO] Data berhasil disimpan ke tabel '{table_name}'!")

    except Exception as e:
        print(f"[ERROR] Gagal menyimpan ke PostgreSQL: {e}")
        raise