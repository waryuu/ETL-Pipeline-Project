import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
import requests

from utils.extract import scrape_collection_data, fetch_page_content, extract_collection_data


class TestExtractFunctions(unittest.TestCase):

    def setUp(self):
        """Setup URL dasar untuk test"""
        self.url = "https://fashion-studio.dicoding.dev/"

    # ================================
    # TEST fetch_page_content
    # ================================

    @patch('utils.extract.requests.get')
    def test_fetch_page_content_success(self, mock_get):
        """Test fetch_page_content berhasil mengembalikan HTML jika request sukses"""

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><h1>Mock Content Page</h1></body></html>"
        mock_get.return_value = mock_response

        result = fetch_page_content("http://dummy-url.com")

        self.assertIn("Mock Content Page", result)

    @patch('utils.extract.requests.get')
    def test_fetch_page_content_failure(self, mock_get):
        """Test fetch_page_content mengembalikan None jika request gagal"""

        mock_get.side_effect = requests.exceptions.RequestException("Gagal mengambil halaman")

        result = fetch_page_content(self.url)

        self.assertIsNone(result)

    # ================================
    # TEST extract_collection_data
    # ================================

    def test_extract_collection_data_valid(self):
        """Test extract_collection_data dari HTML dengan struktur asli"""

        html = """
        <div class="collection-card">
            <div class="product-details">
                <h3 class="product-title">T-shirt 2</h3>
                <div class="price-container">
                    <span class="price">$102.15</span>
                </div>
                <p>Rating: ⭐ 3.9 / 5</p>
                <p>3 Colors</p>
                <p>Size: M</p>
                <p>Gender: Women</p>
            </div>
        </div>
        """

        div = BeautifulSoup(html, "html.parser").find("div", class_="collection-card")
        result = extract_collection_data(div)

        self.assertEqual(result["Title"], "T-shirt 2")
        self.assertEqual(result["Price"], "$102.15")
        self.assertEqual(result["Rating"], "3.9")
        self.assertEqual(result["Colors"], "3 Colors")
        self.assertEqual(result["Size"], "M")
        self.assertEqual(result["Gender"], "Women")
        self.assertIn("Timestamp", result)

    def test_extract_collection_data_invalid_rating(self):
        """Test extract_collection_data dengan rating invalid"""

        html = """
        <div class="collection-card">
            <div class="product-details">
                <h3 class="product-title">Unknown Product</h3>
                <div class="price-container">
                    <span class="price">$100.00</span>
                </div>
                <p>Rating: ⭐ Invalid Rating / 5</p>
                <p>5 Colors</p>
                <p>Size: M</p>
                <p>Gender: Men</p>
            </div>
        </div>
        """

        div = BeautifulSoup(html, "html.parser").find("div", class_="collection-card")
        result = extract_collection_data(div)

        self.assertEqual(result["Title"], "Unknown Product")
        self.assertIsNone(result["Rating"])  # sesuai logic ideal untuk invalid rating

    # ================================
    # TEST scrape_collection_data
    # ================================

    @patch('utils.extract.fetch_page_content')
    def test_scrape_collection_data_one_product(self, mock_fetch):
        """Test scrape_collection_data mengembalikan list dengan 1 produk"""

        mock_html = """
        <html><body>
            <div class="collection-card">
                <div class="product-details">
                    <h3 class="product-title">Sweater Percobaan</h3>
                    <div class="price-container">
                        <span class="price">$100.67</span>
                    </div>
                    <p>Rating: ⭐ 4.4 / 5</p>
                    <p>2 Colors</p>
                    <p>Size: L</p>
                    <p>Gender: Unisex</p>
                </div>
            </div>
        </body></html>
        """

        mock_fetch.return_value = mock_html

        result = scrape_collection_data(self.url, 1)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Title"], "Sweater Percobaan")

    @patch('utils.extract.fetch_page_content')
    def test_scrape_collection_data_no_products(self, mock_fetch):
        """Test scrape_collection_data mengembalikan list kosong jika tidak ada card"""

        mock_fetch.return_value = "<html><body><p>Halaman kosong</p></body></html>"

        result = scrape_collection_data(self.url)

        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()