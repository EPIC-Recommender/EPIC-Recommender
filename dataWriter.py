from typing import Optional, List, Union
import psycopg2

class MovieDatabaseWriter:
    """this class should not be used for more than one movie after Inserting
       a movie and the other data for that movie you should create another object
       to add a new movie
    """
    def __init__(self, dbname: str, user: str, password: str, host: str = 'localhost', port: int = 5432) -> None:

        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cur = self.conn.cursor()
        self.current_movie_id = -1

    def close_connection(self) -> None:

        self.cur.close()
        self.conn.close()

    def insert_movie(self, title: str, movei_awards: Optional[int] = None, imdb_rating: Optional[float] = None,
                     rotten_rating: Optional[float] = None, meta_rating: Optional[float] = None, pg_rating: Optional[str] = None,
                     genre: Optional[List[str]] = None) -> int:

        sql = """INSERT INTO public.movie ("Title", movei_awards, imdb_rating, rotten_rating, meta_rating, pg_rating, genre)
                 VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING "ID";"""
        values = (title, movei_awards, imdb_rating, rotten_rating, meta_rating, pg_rating, genre)
        self.cur.execute(sql, values)
        # movie_id_row = self.cur.fetchone()
        # if movie_id_row:
        #     movie_id = movie_id_row[0]
        #     self.conn.commit()
        #     self.current_movie_id = movie_id
        #     return movie_id
        # else:
        #     print("insert movie no id")
        #     return -1
        self.current_movie_id = self.cur.lastrowid
        return self.current_movie_id

    def insert_person(self, name: str, gender: Optional[bool] = None, nationality: Optional[str] = None,
                      dob: Optional[str] = None) -> None:

        sql = """INSERT INTO public.person ("Name", gender, nationality, "DOB")
                 VALUES (%s, %s, %s, %s)"""
        values = (name, gender, nationality, dob)
        self.cur.execute(sql, values)
        self.conn.commit()

#TODO make the parts after this line work
    def insert_director(self, name: str, gender: Optional[bool] = None, nationality: Optional[str] = None,
                      dob: Optional[str] = None) -> None:

        self.insert_person(name, gender, nationality, dob)
        director_id = self.cur.lastrowid  # Assuming "ID" is serial and auto-incremented
        self.insert_movie_director(movie_id=movie_id, director_id=director_id)

    def insert_movie_actor(self, movie_id: int, actor_id: int) -> None:

        sql = """INSERT INTO public.movie_actor (movie, actor)
                 VALUES (%s, %s)"""
        values = (movie_id, actor_id)
        self.cur.execute(sql, values)
        self.conn.commit()

    def insert_actor(self, name: str, gender: Optional[bool] = None, nationality: Optional[str] = None,
                    dob: Optional[str] = None) -> None:
        self.insert_person(name, gender, nationality, dob)
        actor_id = self.cur.lastrowid  # Assuming "ID" is serial and auto-incremented
        self.insert_movie_actor(movie_id=self.current_movie_id, actor_id=actor_id)

    def insert_movie_director(self, movie_id: int, director_id: int) -> None:
        sql = """INSERT INTO public.movie_director (movie, director)
                 VALUES (%s, %s)"""
        values = (movie_id, director_id)
        self.cur.execute(sql, values)
        self.conn.commit()

# Example usage:
writer = MovieDatabaseWriter(dbname='EpicDB', user='postgres', password='')

# Inserting a movie and retrieving its ID
writer.insert_movie(title='The Shawshank Redemption', imdb_rating=9)

# Inserting an actor
# writer.insert_actor(name='Tim Robbins', dob='1958-10-16')

# Inserting a director
# writer.insert_director(name='Frank Darabont', dob='1959-01-28')

# Don't forget to close the connection when done
# writer.close_connection()
       
