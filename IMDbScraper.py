import json
import requests
from bs4 import BeautifulSoup
import urllib.parse

class IMDbScraper:
    def __init__(self):
        self.base_url = "https://www.imdb.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def get_movie_rating(self, movie_title):
        # IMDb'den film araması yap
        search_url = f"{self.base_url}/find?q={urllib.parse.quote_plus(movie_title)}&s=tt"
        print("Arama URL'si:", search_url)  # Arama URL'sini yazdır
        response = requests.get(search_url, headers=self.headers)

        if response.status_code != 200:
            print(f"Arama isteği başarısız oldu: {response.status_code}")
            return None

        # İlk filmi bul ve IMDb sayfasına git
        soup = BeautifulSoup(response.text, 'html.parser')
        first_result = soup.find('a', class_='ipc-metadata-list-summary-item__t')
        if first_result:
            movie_id = first_result['href'].split('/')[2]
        else:
            print(f"Film '{movie_title}' için sonuç bulunamadı")
            return None

        movie_url = f"{self.base_url}/title/{movie_id}/"
        movie_page_response = requests.get(movie_url, headers=self.headers)

        if movie_page_response.status_code != 200:
            print(f"Film sayfasına erişim başarısız oldu: {movie_page_response.status_code}")
            return None

        # IMDb sayfasından film ratingini çek
        rating = self._parse_movie_page(movie_page_response.text)
        return rating

    def _parse_movie_page(self, html):
        # HTML'den film ratingini çek
        soup = BeautifulSoup(html, 'html.parser')
        rating_span = soup.find('span', class_='sc-bde20123-1 cMEQkK')
        if rating_span:
            try:
                rating = float(rating_span.text.strip())
                return rating
            except ValueError:
                print(f"Film sayfasından puan alınamadı: {rating_span.text.strip()}")
                return None
        else:
            print("IMDb puanı bulunamadı.")
            return None

# JSON dosyasını oku (doğru encoding ile)
try:
    with open('10000movies.json', 'r', encoding='UTF-8') as f:
        movies_data = json.load(f)
except UnicodeDecodeError:
    print("JSON dosyası UTF-8 ile kodlanmamış olabilir. Farklı bir encoding deneyin.")
    exit(1)

scraper = IMDbScraper()

# Her bir film için IMDb ratingini çek ve JSON verisine ekle
for movie_data in movies_data:
    film_title = movie_data.get('Film_title', '')
    rating = scraper.get_movie_rating(film_title)
    if rating is not None:
        movie_data['IMDb_rating'] = rating
        print("JSON dosyası güncellendi.")
    else:
        movie_data['IMDb_rating'] = "Bulunamadı"  # IMDb puanı bulunamazsa

# Güncellenmiş veriyi başka bir dosyaya yaz
with open('10000movies1.json', 'w', encoding='UTF-8') as f:
    json.dump(movies_data, f, ensure_ascii=False, indent=4)
