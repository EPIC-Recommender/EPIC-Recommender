from typing import Optional, List, Union
from abc import ABC, abstractmethod
import psycopg2

class DataHolder(ABC):
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def write(db):
        pass

class MovieData:
    """this class holds the scraped data of movies."""
    def __init__(self):
        pass

class DataWriter():
    """Uses Data classes to write to the data base."""
    def __init__(self):
        pass
            
        
