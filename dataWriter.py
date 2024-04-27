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
        self.current_movie_id = self.get_last_inserted_id()
        self.conn.commit()
        return self.current_movie_id

    def insert_person(self, name: str, gender: Optional[bool] = None, nationality: Optional[str] = None,
                      dob: Optional[str] = None) -> int:

        sql = """INSERT INTO public.person ("Name", gender, nationality, "DOB")
                 VALUES (%s, %s, %s, %s)"""
        values = (name, gender, nationality, dob)
        self.cur.execute(sql, values)
        id = self.get_last_inserted_id()
        self.conn.commit()
        return id


    def insert_director(self, name: str, gender: Optional[bool] = None, nationality: Optional[str] = None,
                      dob: Optional[str] = None) -> None:

        director_id = self.insert_person(name, gender, nationality, dob)
        try:
            self.insert_movie_director(movie_id=self.current_movie_id, director_id=director_id)
        except Exception:
            print("error at insert_person make sure the movie_id and director_id correct")


    def insert_actor(self, name: str, gender: Optional[bool] = None, nationality: Optional[str] = None,
                    dob: Optional[str] = None) -> None:

        actor_id = self.insert_person(name, gender, nationality, dob)
        try:
            self.insert_movie_actor(movie_id=self.current_movie_id, actor_id=actor_id)
        except Exception:
            print("error at insert_person make sure the movie_id and director_id correct")

    def insert_award(self, name:str,date:str) -> int:
        sql = """INSERT INTO public.award ("name","date")
                 VALUES (%s,%s)"""
        values = (name,date)
        self.cur.execute(sql,values)
        id = self.get_last_inserted_id()
        self.conn.commit()
        return id

    def insert_genre(self, genre_name: str) -> int:
        sql = """INSERT INTO public.genre (genre_name)
                 VALUES (%s) RETURNING genre_id;"""
        values = (genre_name,)
        self.cur.execute(sql, values)
        genre_id = self.get_last_inserted_id()
        self.conn.commit()
        self.insert_movie_genre(self.current_movie_id, genre_id)
        return genre_id

    def insert_synopsis(self,synopsis_text: str) -> int:
        sql = """INSERT INTO public.synopsis (synopsis)
                 VALUES (%s);"""
        values = (synopsis_text,)
        self.cur.execute(sql, values)
        synopsis_id = self.get_last_inserted_id()
        self.conn.commit()
        self.insert_movie_synopsis(self.current_movie_id, synopsis_id)
        return synopsis_id
    
#TODO add award inserts 
    def insert_movie_synopsis(self, movie_id: int, synopsis_id: int) -> None:
        sql = """INSERT INTO public.movie_synopsis (movie, synopsis)
                VALUES (%s, %s)"""
        values = (movie_id, synopsis_id)
        self.cur.execute(sql, values)
        self.conn.commit()

    def insert_movie_genre(self, movie_id: int, genre_id: int) -> None:
        sql = """INSERT INTO public.movie_genre (movie_id, genre_id)
                 VALUES (%s, %s)"""
        values = (movie_id, genre_id)
        self.cur.execute(sql, values)
        self.conn.commit()

    def insert_movie_actor(self, movie_id: int, actor_id: int) -> None:

        sql = """INSERT INTO public.movie_actor (movie, actor)
                 VALUES (%s, %s)"""
        values = (movie_id, actor_id)
        self.cur.execute(sql, values)
        self.conn.commit()

    def insert_movie_director(self, movie_id: int, director_id: int) -> None:
        sql = """INSERT INTO public.movie_director (movie, director)
                 VALUES (%s, %s)"""
        values = (movie_id, director_id)
        self.cur.execute(sql, values)
        self.conn.commit()

    def insert_movie_award(self,movie_id:int, award_id:int):
        sql = """INSERT INTO public.movie_award( "award_ID", "movie_ID")
                 VALUES (%s,%s)"""
        values = (award_id,movie_id)
        self.cur.execute(sql,values)
        self.conn.commit

    def insert_person_award(self,person_id:int, award_id:int):
        sql = """INSERT INTO public.award_person( "award_ID", "person_ID")
                 VALUES (%s,%s)"""
        values = (award_id,person_id)
        self.cur.execute(sql,values)
        self.conn.commit

    def get_last_inserted_id(self) -> int:

        self.cur.execute("SELECT LASTVAL();")
        row = self.cur.fetchone()

        if row:
            return row[0]
        else:
            return -1
if __name__ == "__main__":
# Example usage:
    writer = MovieDatabaseWriter(dbname='EpicDB', user='postgres', password='')
# Inserting a movie and retrieving its ID
    movie_id = writer.insert_movie(title='The Shawshank Redemption', imdb_rating=9)
# Inserting an actor
    writer.insert_actor(name='Tim Robbins', dob='1958-10-16')
# Inserting a director
    writer.insert_director(name='Frank Darabont', dob='1959-01-28')
# Inserting a genre and associating it with the movie
    genre_id = writer.insert_genre(genre_name='Drama')
# Inserting a synopsis and associating it with the movie
    synopsis_id = writer.insert_synopsis(synopsis_text='Two imprisoned men bond over a number of years, finding solace and common decency.')
# Inserting an award
    award_id = writer.insert_award(name='Oscar', date='1995-03-27')
# Don't forget to close the connection when done
    writer.close_connection()
        
