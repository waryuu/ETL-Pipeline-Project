import pandas as pd
import numpy as np
from datetime import datetime

USD_TO_IDR = 16000


# -----------------------------
# Transform Functions
# -----------------------------
def transform_to_DataFrame(data):
    """Mengubah data list of dictionary menjadi pandas DataFrame."""
    try:
        return pd.DataFrame(data)
    except Exception as e:
        print(f"[ERROR] Gagal mengubah data menjadi DataFrame: {e}")
        return pd.DataFrame()

def transform_title(df):
    """Membersihkan kolom Title (strip whitespace)."""
    try:
        if 'Title' in df.columns:
            df['Title'] = df['Title'].astype('object')
            df['Title'] = df['Title'].str.strip()
        return df
    except Exception as e:
        print(f"[ERROR] Gagal transform Title: {e}")
        return df
    
def transform_price(df):
    """
    Membersihkan kolom Price:
    - Menghapus simbol $
    - Mengubah ke float
    - Konversi USD ke IDR
    """
    try:
        if 'Price' in df.columns:
            df['Price'] = df['Price'].replace(['Price Unavailable', None], np.nan)
            df['Price'] = df['Price'].str.replace('$', '', regex=False).str.replace(',', '', regex=False)
            df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
            df['Price'] = df['Price'] * USD_TO_IDR
        return df
    except Exception as e:
        print(f"[ERROR] Gagal transform Price: {e}")
        return df

def transform_rating(df):
    """
    Membersihkan kolom Rating dan mengubah ke float.
    """
    try:
        if 'Rating' in df.columns:
            df['Rating'] = df['Rating'].replace(['Price Unavailable', 'Not Rated', None], np.nan)
            df['Rating'] = df['Rating'].str.extract(r'(\d+\.?\d*)')
            df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
        return df
    except Exception as e:
        print(f"[ERROR] Gagal transform Rating: {e}")
        return df

def transform_color(df):
    """
    Membersihkan kolom Colors dan mengubah menjadi integer nullable.
    """
    try:
        if 'Colors' in df.columns:
            df['Colors'] = df['Colors'].str.replace(
                r'Colors', '', regex=True
            ).str.strip()
            df['Colors'] = pd.to_numeric(
                df['Colors'], errors='coerce'
            ).astype('Int64')
        return df
    except Exception as e:
        print(f"[ERROR] Gagal transform Colors: {e}")
        return df

def transform_size_and_gender(df):
    """
    Standarisasi format Size dan Gender.
    """
    try:
        if 'Size' in df.columns:
            df['Size'] = df['Size'].astype('object')
            df['Size'] = df['Size'].str.upper().str.strip()

        if 'Gender' in df.columns:
            df['Gender'] = df['Gender'].astype('object')
            df['Gender'] = df['Gender'].str.capitalize().str.strip()

        return df
    except Exception as e:
        print(f"[ERROR] Gagal transform Size/Gender: {e}")
        return df

def transform_timestamp(df):
    """
    Mengubah kolom Timestamp menjadi tipe datetime.
    """
    try:
        if 'Timestamp' in df.columns:
            df['Timestamp'] = pd.to_datetime(
                df['Timestamp'], errors='coerce'
            )
        return df
    except Exception as e:
        print(f"[ERROR] Gagal transform Timestamp: {e}")
        return df


# -----------------------------
# Clean Functions
# -----------------------------
def clean_duplicates(df, subset=None):
    """
    Menghapus baris duplikat berdasarkan subset kolom.
    Default: semua kolom.
    """
    try:
        return df.drop_duplicates(subset=subset, keep='first')
    except Exception as e:
        print(f"[ERROR] Gagal menghapus duplikat: {e}")
        return df


def clean_missing_data(df):
    """
    Menghapus baris yang memiliki nilai missing (NaN).
    """
    try:
        return df.dropna()
    except Exception as e:
        print(f"[ERROR] Gagal menghapus missing data: {e}")
        return df

# -----------------------------
# Main Transform Function
# -----------------------------
def transform(data):
    """
    Pipeline utama transformasi data:
    1. Convert ke DataFrame
    2. Bersihkan setiap kolom
    3. Hapus missing value
    4. Hapus duplikat
    """

    try:
        df = transform_to_DataFrame(data)

        # Terapkan transformasi berurutan
        df = transform_title(df)
        df = transform_price(df)
        df = transform_rating(df)
        df = transform_color(df)
        df = transform_size_and_gender(df)
        df = transform_timestamp(df)

        # Bersihkan data
        df = clean_missing_data(df)
        df = clean_duplicates(df)

        return df

    except Exception as e:
        print(f"[ERROR] Terjadi kegagalan dalam pipeline transform: {e}")
        return pd.DataFrame()