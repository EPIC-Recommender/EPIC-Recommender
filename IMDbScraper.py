import requests
from bs4 import BeautifulSoup
import pandas as pd

def search_imdb(title):
    """ Searches IMDb using the title and returns the ID of the first result. """
    query = "+".join(title.split())
    url = f"https://www.imdb.com/find?q={query}&s=tt&ttype=ft"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        title_link = soup.find('td', class_='result_text').a['href']
        imdb_id = title_link.split('/')[2]
        return imdb_id
    except Exception as e:
        print(f"Error in IMDb search: {e}")
        return None

def get_imdb_rating(imdb_id):
    """ Fetches the IMDb rating for a given IMDb ID. """
    if imdb_id is None:
        return 'N/A'
    url = f"https://www.imdb.com/title/{imdb_id}/"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        rating = soup.find('span', itemprop='ratingValue')
        if rating:
            return rating.text
        else:
            return 'N/A'
    except Exception as e:
        print(f"Error fetching IMDb rating: {e}")
        return 'N/A'

def get_movie_ratings(title):
    """ Retrieves the IMDb rating for a given film title. """
    imdb_id = search_imdb(title)
    imdb_rating = get_imdb_rating(imdb_id)
    return imdb_rating

if __name__ == "__main__":
    # Read JSON file
    df = pd.read_json('10000movies.json')

    # Add ratings to DataFrame
    df['IMDb Rating'] = df['Film_title'].apply(get_movie_ratings)

    # Save updated data to a JSON file
    df.to_json('Updated_Movies_With_Ratings.json', orient='records', lines=True)
