import json
from pathlib import Path
import DBconnection
import dataWriter
DBNAME = DBconnection.NAME
PASSWORD = DBconnection.PASSWORD
USER = DBconnection.USER
class MovieDataHandler:

    def __init__(self, path, datawriter:dataWriter.MovieDatabaseWriter):
        self.path = path
        self.datawriter = datawriter
        self.insertedMovieCount = 0

    def process_movies(self):
        # Load JSON data from file
        input_path = Path(self.path)
        with open(input_path, 'r') as f:
            movies_data = json.load(f)

        # Process each movie
        for movie_data in movies_data:
            self._process_movie(movie_data)

    def _process_movie(self, movie_data):
        if isinstance(movie_data,list):
            return
        # Extract movie details
        film_title = movie_data.get('Film_title', '')
        film_synopsis = movie_data.get('Synopsis', '')
        #film_release_year = movie_data.get('Release_year', '')
        #film_director = movie_data.get('Director', '')
        film_cast = movie_data.get('Cast',[])
        film_rating = movie_data.get('Average_rating', -1)
        film_genres = movie_data.get('Genres', [])

        self.datawriter.insert_movie(film_title,meta_rating = film_rating)
        self.datawriter.insert_synopsis(film_synopsis)
        self._insert_movie_cast(film_cast)
        self._insert_movie_genres(film_genres)
        self.insertedMovieCount += 1

    def _insert_movie_cast(self,cast: list[str]):
        if cast is None:
            return
        for actor in cast:
            if actor:
                self.datawriter.insert_actor(actor)


    def _insert_movie_genres(self,genres: list[str]):
        if genres is None:
            return
        for genre in genres:
            if genre:
                self.datawriter.insert_genre(genre)


if __name__ == "__main__":
    # Example usage
    writer = dataWriter.MovieDatabaseWriter(DBNAME,USER,PASSWORD)
    handler = MovieDataHandler('10000movies.json',writer)
    handler.process_movies()
    print(handler.insertedMovieCount)

