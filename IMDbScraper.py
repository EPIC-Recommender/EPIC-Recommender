import json
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

class IMDbScraper:
    def __init__(self):
        self.base_url = "https://www.imdb.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/Version"
        }

    def get_movie_rating(self, movie_title):
        # IMDb search for movie
        search_url = f"{self.base_url}/find?q={urllib.parse.quote_plus(movie_title)}&s=tt"
        print("Arama URL'si:", search_url)

        try:
            response = requests.get(search_url, headers=self.headers)
        except requests.exceptions.RequestException as e:
            print(f"Arama isteği başarısız oldu: {e}")
            return None

        if response.status_code != 200:
            print(f"Arama isteği başarısız oldu: {response.status_code}")
            return None

        # Extract movie ID from first search result
        soup = BeautifulSoup(response.text, 'html.parser')
        first_result = soup.find('a', class_='ipc-metadata-list-summary-item__t')
        if first_result:
            movie_id = first_result['href'].split('/')[2]
        else:
            print(f"Film '{movie_title}' için sonuç bulunamadı")
            return None

        movie_url = f"{self.base_url}/title/{movie_id}/"

        # Add a delay to avoid rate limiting
        time.sleep(2)

        try:
            movie_page_response = requests.get(movie_url, headers=self.headers)
        except requests.exceptions.RequestException as e:
            print(f"Film sayfasına erişim başarısız oldu: {e}")
            return None

        if movie_page_response.status_code != 200:
            print(f"Film sayfasına erişim başarısız oldu: {response.status_code}")
            return None

        # Extract and add rating to movie data
        rating = self._parse_movie_page(movie_page_response.text)
        if rating is not None:
            return rating
        else:
            print("IMDb puanı bulunamadı.")
            return None

    def _parse_movie_page(self, html):
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
            return None

# Read JSON data with UTF-8 encoding
try:
    with open('10000movies.json', 'r', encoding='UTF-8') as f:
        movies_data = json.load(f)
except UnicodeDecodeError:
    print("JSON dosyası UTF-8 ile kodlanmamış olabilir. Farklı bir encoding deneyin.")
    exit(1)

scraper = IMDbScraper()

# Update each movie with IMDb rating (if found)
updated_movies_data = []
for movie in movies_data:
    movie_title = movie['Film_title']
    rating = scraper.get_movie_rating(movie_title)
    if rating is not None:
        movie['IMDb_rating'] = rating
    updated_movies_data.append(movie)

# Write updated data to new JSON file
with open('UWIMDb10000.json', 'w', encoding='UTF-8') as f:
    json.dump(updated_movies_data, f, ensure_ascii=False, indent=4)

print("data added on UWIMDb10000.json")
