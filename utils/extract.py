import requests
from bs4 import BeautifulSoup
from datetime import datetime

# -----------------------------------
# HTTP Headers
# -----------------------------------
# Tambahkan user-agent ke dalam header untuk menghindari blokir oleh server
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

# -----------------------------------
# Extract Product Data
# -----------------------------------
def extract_collection_data(div):
    timestamp = datetime.now().isoformat()

    try:
        # Mengambil Title
        title_tag = div.find("h3", class_="product-title")
        product_title = title_tag.get_text(strip=True) if title_tag else None
        
        # Mengambil Data Price
        price_tag = div.find("span", class_="price")
        price = price_tag.get_text(strip=True) if price_tag else None

        # Mengambil informasi tambahan dari tag <p>
        p_tags = div.find_all("p")
        
        rating = None
        colors = None
        size = None
        gender = None

        if len(p_tags) > 0 and p_tags[0].text:
            rating_text = p_tags[0].text.strip()

            try:
                # Format: "Rating: ⭐ 3.9 / 5"
                rating_part = rating_text.split("⭐")[1]
                rating_value = rating_part.split("/")[0].strip()

                # Validasi apakah angka
                rating = str(float(rating_value))
            except:
                rating = None

        if len(p_tags) > 1 and p_tags[1].text:
            colors = p_tags[1].text.strip()

        if len(p_tags) > 2 and p_tags[2].text:
            size = p_tags[2].text.strip().replace("Size: ", "")

        if len(p_tags) > 3 and p_tags[3].text:
            gender = p_tags[3].text.strip().replace("Gender: ", "")

        return {
            "Title": product_title,
            "Price": price,
            "Rating": rating,
            "Colors": colors,
            "Size": size,
            "Gender": gender,
            "Timestamp": timestamp
        }

    except Exception as e:
        print(f"[ERROR] Gagal ekstraksi data produk: {e}")

        # Return default value agar pipeline tidak berhenti
        return {
            "Title": None,
            "Price": None,
            "Rating": None,
            "Colors": None,
            "Size": None,
            "Gender": None,
            "Timestamp": timestamp
        }

# -----------------------------------
# Fetch Page Content
# -----------------------------------
def fetch_page_content(url):
    """
    Mengambil konten HTML dari URL.
    Menggunakan custom headers dan timeout untuk keamanan request.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()  # Raise error jika status code bukan 200
        return response.text

    except requests.exceptions.Timeout:
        print(f"[ERROR] Timeout saat mengakses {url}")

    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Koneksi gagal ke {url}")

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request error pada {url}: {e}")

    return None

# -----------------------------
# Scrape Collection Function
# -----------------------------
def scrape_collection_data(url, max_pages=50):
    """
    Melakukan scraping seluruh halaman koleksi produk.

    Parameter:
    - url: URL utama koleksi
    - max_pages: batas maksimal halaman yang akan discrape

    Return:
    - List of dictionary berisi data produk
    """

    data = []
    page = 1  # Mulai dari halaman pertama

    try:
        while page <= max_pages:
            # Mendefinisikan url untuk setiap halaman yang akan di scraping
            current_url = url if page == 1 else f"{url}/page{page}"  # Selain pada page pertama, diberi prefix /{page}

            content = fetch_page_content(current_url)
            if not content:
                print(f"[INFO] Tidak ada content di halaman {page}, berhenti.")
                break

            soup = BeautifulSoup(content, 'html.parser')
            cards = soup.find_all('div', class_='collection-card') # mencari elemen produk di dalam class 'collection-card'

            if not cards: # berhenti scraping jika tidak ada produk
                print(f"[INFO] Tidak ada produk di halaman {page}, berhenti.")
                break

            print(f"[INFO] Scraping halaman {page} ({len(cards)} produk)")
            
            # Ambil data produk dari setiap card
            for card in cards:
                collection_data = extract_collection_data(card)
                if collection_data:  # skip jika None
                    data.append(collection_data)

            page += 1 # melanjutkan ke halaman berikutnya

    except Exception as e:
        print(f"[ERROR] Terjadi error saat scraping: {e}")

    return data