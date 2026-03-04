import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load import store_to_csv, store_to_spreadsheet, create_database, store_to_postgre


class TestLoadFunctions(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            "Title": ["A"],
            "Price": [100],
            "Rating": [4.5],
            "Colors": [2],
            "Size": ["M"],
            "Gender": ["Women"],
            "Timestamp": ["2026-03-04 10:00:00"]
        })

        self.spreadsheet_id = "dummy_spreadsheet_id"
        self.worksheet_name = "Sheet1"

    # ===============================
    # CSV
    # ===============================

    @patch("pandas.DataFrame.to_csv")
    def test_store_to_csv(self, mock_to_csv):
        store_to_csv(self.df, "products.csv")
        mock_to_csv.assert_called_once_with("products.csv", index=False)

    # ===============================
    # Google Spreadsheet
    # ===============================

    @patch("utils.load.gspread.authorize")
    @patch("utils.load.set_with_dataframe")
    @patch("utils.load.ServiceAccountCredentials.from_json_keyfile_name")
    def test_store_to_spreadsheet(self, mock_from_json, mock_authorize, mock_set):
        mock_client = MagicMock()
        mock_spreadsheet = MagicMock()
        mock_worksheet = MagicMock()

        mock_client.open_by_key.return_value = mock_spreadsheet
        mock_spreadsheet.worksheet.return_value = mock_worksheet
        mock_authorize.return_value = mock_client

        store_to_spreadsheet(self.df, self.spreadsheet_id, self.worksheet_name, "dummy_credentials.json")

        mock_authorize.assert_called_once()
        mock_set.assert_called_once()

    # ===============================
    # PostgreSQL - Create Database
    # ===============================

    @patch("utils.load.psycopg2.connect")
    def test_create_database(self, mock_connect):

        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        create_database("test_db")

        print(mock_cursor.execute.call_args_list)

        mock_cursor.execute.assert_any_call(
            "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s",
            ("test_db",)
    )
        
    # ===============================
    # PostgreSQL - Insert Data
    # ===============================

    @patch("utils.load.create_engine")
    @patch("pandas.DataFrame.to_sql")
    def test_store_to_postgre(self, mock_to_sql, mock_engine):

        mock_engine_instance = MagicMock()
        mock_engine.return_value = mock_engine_instance

        store_to_postgre(self.df, "postgresql://user:pass")

        mock_engine.assert_called_once()
        mock_to_sql.assert_called_once()


if __name__ == "__main__":
    unittest.main()