import json
import requests
from bs4 import BeautifulSoup
import urllib.parse

class BeyazPerdeScraper:
    def __init__(self):
        self.base_url = "https://www.beyazperde.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/Version"
        }

    def get_movie_rating(self, movie_title):
        search_url = f"{self.base_url}/aramak/?q={urllib.parse.quote_plus(movie_title)}"
        print("Search URL:", search_url)

        try:
            response = requests.get(search_url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Search request failed: {e}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        # Find elements in the search results for the movie
        result_items = soup.find_all('div', class_='card entity-card entity-card-list cf')

        if result_items:
            for result in result_items:
                # Find the element containing the rating (the third stareval-note)
                rating_elements = result.find_all('span', class_='stareval-note')
                if len(rating_elements) >= 3:
                    try:
                        rating = float(rating_elements[2].text.strip().replace(',', '.'))
                        return rating * 2  # Multiply rating by 2
                    except ValueError:
                        print(f"Rating could not be extracted: {rating_elements[2].text.strip()}")
                        return None
            print(f"Rating not found for the movie '{movie_title}'")
            return None
        else:
            print(f"No results found for the movie '{movie_title}'")
            return None

try:
    with open('UWIMDb10000.json', 'r', encoding='UTF-8') as f:
        movies_data = json.load(f)
except UnicodeDecodeError:
    print("The JSON file might not be encoded in UTF-8. Try a different encoding.")
    exit(1)

scraper = BeyazPerdeScraper()
updated_movies_data = []
for movie in movies_data:
    movie_title = movie['Film_title']
    print(f"Processing movie: {movie_title}")
    rating = scraper.get_movie_rating(movie_title)
    if rating is not None:
        movie['BeyazPerde_rating'] = rating
    updated_movies_data.append(movie)

with open('AllFilms.json', 'w', encoding='UTF-8') as f:
    json.dump(updated_movies_data, f, ensure_ascii=False, indent=4)

print("Data added on AllFilms.json")
