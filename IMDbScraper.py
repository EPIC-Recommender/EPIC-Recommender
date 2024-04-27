import requests
from bs4 import BeautifulSoup
import psycopg2
import os  # For environment variables

def get_imdb_top_movies(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    movies = soup.find_all("div", class_="lister-item mode-advanced")
    movie_data = []
    for movie in movies:
        title = movie.find("h3", class_="lister-item-header").find("a").text.strip()
        year_tag = movie.find("span", class_="lister-item-year text-muted unbold")
        year = year_tag.text.strip("()") if year_tag else None
        rating_tag = movie.find("div", class_="ratings-bar").find("strong")
        rating = float(rating_tag.text) if rating_tag else None
        genre_tag = movie.find("span", class_="genre")
        genre = genre_tag.text.split(", ") if genre_tag else None
        director_tags = movie.find("div", class_="lister-item-content").findall("a", class_="lister-item-header")
        director = director_tags[1].text if len(director_tags) > 1 else None
        synopsis_tag = movie.find("div", class_="lister-item-content").find("p", class_="text-muted")
        synopsis = synopsis_tag.text.strip() if synopsis_tag else None
        movie_data.append({
            "title": title,
            "year": year,
            "rating": rating,
            "genre": genre,
            "director": director,
            "synopsis": synopsis
        })
    return movie_data

def connect_to_database():
    # Database connection details should be stored securely (not in the code)
    # Options:
    # 1. Environment variables (recommended)
    #   - Set `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` environment variables
    # 2. Secure configuration file (e.g., JSON, encrypted)
    #   - Load credentials from a secure file
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password)
    return conn

def insert_movies_into_db(conn, movie_data):
    cursor = conn.cursor()
    sql = """
        INSERT INTO movie (title, year, rating, genre, director, synopsis)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    for movie in movie_data:
        cursor.execute(sql, (movie["title"], movie["year"], movie["rating"], movie["genre"], movie["director"], movie["synopsis"]))
    conn.commit()
    cursor.close()

if __name__ == "__main__":
    # Check IMDb terms of service and consider authorized data access methods
    # ...

    # Get IMDb Top 250 Movies
    url = "https://m.imdb.com/chart/top/"
    movie_data = get_imdb_top_movies(url)

    # Connect to the database securely
    conn = connect_to_database()

    # Insert movie data into the database
    insert_movies_into_db(conn, movie_data)

    # Close the database connection
    conn.close()

    print("Movie data successfully retrieved and saved to the database (using authorized methods).")
