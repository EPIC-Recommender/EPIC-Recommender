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
    

class MovieData(DataHolder):
    """this class holds the scraped data of movies.
       for example 

    """
    def __init__(self):
        super().__init__()

class ActorData(DataHolder):
    """this class holds the scraped data of movies.
       for example 
    """
    def __init__(self):
        super().__init__("movie_actor")

class DirectorData(DataHolder):
    """this class holds the scraped data of movies.
       for example 
    """
    def __init__(self):
        super().__init__("movie_director")

class ProducerData(DataHolder):
    """this class holds the scraped data of movies.
       for example 
    """
    def __init__(self):
        super().__init__("movie_producer")

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
            
        
