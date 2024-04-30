import requests
from bs4 import BeautifulSoup
import psycopg2
from psycopg2.extras import execute_values

# Database connection
conn = psycopg2.connect("dbname=your_db user=your_user password=your_password")
cursor = conn.cursor()

def get_movie_info(movie_title):
    url = f"https://en.wikipedia.org/wiki/{movie_title.replace(' ', '_')}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.find('h1', id='firstHeading').text
    info_box = soup.find('table', class_='infobox')
    imdb_rating, rotten_rating, meta_rating, pg_rating = None, None, None, None
    genres, directors, actors, awards = [], [], [], []
    synopsis_text = ""

    if info_box:
        rows = info_box.find_all('tr')
        for row in rows:
            header = row.find('th')
            if header:
                header_text = header.text.strip()
                data = row.find('td')
                if data:
                    data_text = data.text.strip()
                    if 'Directed by' in header_text:
                        directors = [d.strip() for d in data_text.split(',')]
                    elif 'Starring' in header_text:
                        actors = [a.strip() for a in data_text.split(',')]
                    elif 'Genre' in header_text:
                        genres = [g.strip() for g in data_text.split(',')]
                    elif 'IMDb' in header_text:
                        imdb_rating = data_text
                    elif 'Rotten Tomatoes' in header_text:
                        rotten_rating = data_text
                    elif 'Metacritic' in header_text:
                        meta_rating = data_text
    
    synopsis_section = soup.find('div', class_='mw-parser-output')
    if synopsis_section:
        p_tags = synopsis_section.find_all('p')
        synopsis_text = ' '.join(p.text for p in p_tags[:2])
    
    cursor.execute("INSERT INTO public.movie (Title, imdb_rating, rotten_rating, meta_rating, pg_rating) VALUES (%s, %s, %s, %s, %s) RETURNING ID", (title, imdb_rating, rotten_rating, meta_rating, pg_rating))
    movie_id = cursor.fetchone()[0]
    if genres:
        genre_values = [(movie_id, genre) for genre in genres]
        execute_values(cursor, "INSERT INTO public.movie_genre (movie_id, genre_id) VALUES %s", genre_values)
    if actors:
        actor_values = [(movie_id, actor) for actor in actors]
        execute_values(cursor, "INSERT INTO public.movie_actor (movie, actor) VALUES %s", actor_values)
    if directors:
        director_values = [(movie_id, director) for director in directors]
        execute_values(cursor, "INSERT INTO public.movie_director (movie, director) VALUES %s", director_values)
    if synopsis_text:
        cursor.execute("INSERT INTO public.synopsis (synopsis) VALUES (%s) RETURNING ID", (synopsis_text,))
        synopsis_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO public.movie_synopsis (movie, synopsis) VALUES (%s, %s)", (movie_id, synopsis_id))
    
    conn.commit()

# Example usage
get_movie_info('Inception')

# Close database connection
cursor.close()
conn.close()
