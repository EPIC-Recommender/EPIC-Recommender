from typing import Optional, List, Union
from abc import ABC, abstractmethod
import psycopg2

class DataHolder(ABC):
    """This is an abstract class for data holders
    
    Args:
        name(str) which many to many table the class should be connected to 
        example "movie_actor"
    """
    def __init__(self,name = None) -> None:
        self.name = name
        pass
    
class GenreData(DataHolder):
    """this class holds the scraped data of movies.
       for example 
    """
    def __init__(self,genre=None):
        super().__init__("movie_genre")
        self.genre = genre

class MovieData(DataHolder):
    """this class holds the scraped data of movies.
       for example 
    """
    def __init__(self,
                 title: str,
                 imdb_rating: int,
                 rotten_rating: int,
                 meta_rating: int,
                 pg_rating: str,
                 ):
        super().__init__()
        self.title = title
        self.imdb_rating = imdb_rating
        self.rotten_rating = rotten_rating
        self.meta_rating = meta_rating
        self.pg_rating = pg_rating

class ActorData(DataHolder):
    """this class holds the scraped data of movies.
       for example 
    """
    def __init__(self,
                 name: str,
                 gender: bool,
                 nationality: str,
                 DOB: str
                 ):
        super().__init__("movie_actor")
        self.name = name
        self.gender = gender
        self.nationality = nationality
        self.DOB = DOB
        
class DirectorData(DataHolder):
    """this class holds the scraped data of movies.
       for example 
    """
    def __init__(self,
                 name: str,
                 gender: bool,
                 nationality: str,
                 DOB: str
                 ):
        super().__init__("movie_director")
        self.name = name
        self.gender = gender
        self.nationality = nationality
        self.DOB = DOB

class ProducerData(DataHolder):
    """this class holds the scraped data of movies.
       for example 
    """
    def __init__(self,
                 name: str,
                 gender: bool,
                 nationality: str,
                 DOB: str
                 ):
        super().__init__("movie_producer")
        self.name = name
        self.gender = gender
        self.nationality = nationality
        self.DOB = DOB

class PersonAwardData(DataHolder):
    """this class holds the scraped data of movies.
       for example 
    """
    def __init__(self):
        super().__init__("award_person") 

class MovieAwardData(DataHolder):
    """this class holds the scraped data of movies.
       for example 
    """
    def __init__(self):
        super().__init__("movie_award")

class SynopsisData(DataHolder):
    """this class holds the scraped data of movies.
       for example 
    """
    def __init__(self):
        super().__init__("movie_producer")

class DataWriter():
    """Uses Data classes to write to the data base."""
    def __init__(self):
        pass
            
        
