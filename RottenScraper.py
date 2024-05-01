import requests
from bs4 import BeautifulSoup
import psycopg2
from psycopg2.extras import execute_values

# Database connection
conn = psycopg2.connect("dbname=your_db user=your_user password=your_password")
cursor = conn.cursor()

def get_movie_info_from_rotten_tomatoes(movie_title):
    base_url = "https://www.rottentomatoes.com/m/"
    url = f"{base_url}{movie_title.replace(' ', '_')}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.find('h1', class_='mop-ratings-wrap__title mop-ratings-wrap__title--top').text.strip()
    tomato_meter = soup.find('span', class_='mop-ratings-wrap__percentage').text.strip()
    audience_score = soup.find('span', class_='mop-ratings-wrap__percentage mop-ratings-wrap__percentage--audience').text.strip()
    
    genre_tags = soup.find_all('span', class_='genre')
    genres = [genre.text.strip() for genre in genre_tags]
    
    director_tags = soup.find_all('li', class_='meta-row clearfix')
    directors = [director.find('a').text.strip() for director in director_tags if 'Directed By' in director.text]
    
    actor_tags = soup.find_all('li', class_='meta-row clearfix')
    actors = [actor.find('a').text.strip() for actor in actor_tags if 'In Theaters' in actor.text]
    
    synopsis = soup.find('div', id='movieSynopsis').text.strip()
    
    cursor.execute("INSERT INTO public.movie (Title, rotten_rating) VALUES (%s, %s) RETURNING ID", (title, tomato_meter))
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
    
    cursor.execute("INSERT INTO public.synopsis (synopsis) VALUES (%s) RETURNING ID", (synopsis,))
    synopsis_id = cursor.fetchone()[0]
    cursor.execute("INSERT INTO public.movie_synopsis (movie, synopsis) VALUES (%s, %s)", (movie_id, synopsis_id))
    
    conn.commit()

# Example usage
get_movie_info_from_rotten_tomatoes('inception')

# Close database connection
cursor.close()
conn.close()