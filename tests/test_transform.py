import unittest
import pandas as pd
import numpy as np
from datetime import datetime

from utils.transform import (
    transform_to_DataFrame,
    transform_price,
    transform_rating,
    transform_color,
    transform_size_and_gender,
    transform_timestamp,
    clean_missing_data,
    clean_duplicates,
    transform,
    USD_TO_IDR
)


class TestTransformFunctions(unittest.TestCase):

    def setUp(self):
        """Sample raw data seperti hasil extract"""
        timestamp = datetime.now().isoformat()
        self.sample_data = [
            {
                "Title": " Kaos Test ",
                "Price": "$10.0",
                "Rating": "4.5",
                "Colors": "3 Colors",
                "Size": "m",
                "Gender": "women",
                "Timestamp": timestamp
            },
            {
                "Title": " Kaos Test ",  # duplicate
                "Price": "$10.0",
                "Rating": "4.5",
                "Colors": "3 Colors",
                "Size": "m",
                "Gender": "women",
                "Timestamp": timestamp
            }
        ]

    # ===============================
    # Individual Transform Tests
    # ===============================

    def test_transform_to_dataframe(self):
        df = transform_to_DataFrame(self.sample_data)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)

    def test_transform_price(self):
        df = pd.DataFrame(self.sample_data)
        df = transform_price(df)

        expected_price = 10.0 * USD_TO_IDR
        self.assertEqual(df.loc[0, "Price"], expected_price)

    def test_transform_rating(self):
        df = pd.DataFrame(self.sample_data)
        df = transform_rating(df)

        self.assertEqual(df.loc[0, "Rating"], 4.5)

    def test_transform_color(self):
        df = pd.DataFrame(self.sample_data)
        df = transform_color(df)

        self.assertEqual(df.loc[0, "Colors"], 3)
        self.assertEqual(str(df["Colors"].dtype), "Int64")

    def test_transform_size_and_gender(self):
        df = pd.DataFrame(self.sample_data)
        df = transform_size_and_gender(df)

        self.assertEqual(df.loc[0, "Size"], "M")
        self.assertEqual(df.loc[0, "Gender"], "Women")

    def test_transform_timestamp(self):
        df = pd.DataFrame(self.sample_data)
        df = transform_timestamp(df)

        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df["Timestamp"]))

    def test_clean_duplicates(self):
        df = pd.DataFrame(self.sample_data)
        df = clean_duplicates(df)

        self.assertEqual(len(df), 1)

    def test_clean_missing_data(self):
        df = pd.DataFrame(self.sample_data)
        df.loc[0, "Price"] = np.nan

        df = clean_missing_data(df)

        self.assertEqual(len(df), 1)

    # ===============================
    # Full Pipeline Test
    # ===============================

    def test_full_transform_pipeline(self):
        df = transform(self.sample_data)

        # Harus jadi 1 row karena duplicate dihapus
        self.assertEqual(len(df), 1)

        # Check type
        self.assertTrue(pd.api.types.is_float_dtype(df["Price"]))
        self.assertTrue(pd.api.types.is_float_dtype(df["Rating"]))
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df["Timestamp"]))

        # Check value
        self.assertEqual(df.iloc[0]["Size"], "M")
        self.assertEqual(df.iloc[0]["Gender"], "Women")


if __name__ == "__main__":
    unittest.main()