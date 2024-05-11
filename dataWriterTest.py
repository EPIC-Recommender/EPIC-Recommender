import unittest
from unittest.mock import patch
import psycopg2
from dataWriter import MovieDatabaseWriter
#Make sure your test db is clean before running existing data will cause not unique errors
class TestMovieDatabaseWriter(unittest.TestCase):
    def setUp(self):
        self.writer = MovieDatabaseWriter('EpicDB', 'postgres', 'root')

    def tearDown(self):
        self.writer.close_connection()

    @patch('psycopg2.connect')
    def test_init(self, mock_connect):
        mock_connect.return_value.cursor.return_value = mock_connect.return_value.cursor()
        writer = MovieDatabaseWriter('EpicDB', 'postgres', 'root')
        self.assertIsNotNone(writer.conn)
        self.assertIsNotNone(writer.cur)
        self.assertEqual(writer.current_movie_id, -1)

    def test_insert_movie(self):
        movie_id = self.writer.insert_movie('Test Movie', 7.5, 80.0, 85.0, 'PG-13')
        self.assertEqual(self.writer.current_movie_id, movie_id)
        self.assertGreater(movie_id, 0)

    def test_insert_person(self):
        person_id = self.writer.insert_person('John Doe', True, 'USA', '1980-01-01')
        self.assertGreater(person_id, 0)

    def test_insert_director(self):
        director_id = self.writer.insert_director('John Doe', True, 'USA', '1980-01-01')
        self.assertGreater(director_id, 0)

    def test_insert_actor(self):
        actor_id = self.writer.insert_actor('Jane Doe', False, 'Canada', '1985-05-15')
        self.assertGreater(actor_id, 0)

    def test_insert_genre(self):
        genre_id = self.writer.insert_genre('Action')
        self.assertGreater(genre_id, 0)

    def test_insert_synopsis(self):
        synopsis_id = self.writer.insert_synopsis('This is a test synopsis.')
        self.assertGreater(synopsis_id, 0)

    def test_insert_award(self):
        award_id = self.writer.insert_award('Best Picture', '2022-01-01')
        self.assertGreater(award_id, 0)

    def test_insert_movie_synopsis(self):
        movie_id = self.writer.insert_movie('Test Movie')
        synopsis_id = self.writer.insert_synopsis('This is a test synopsis.')
        self.writer.insert_movie_synopsis(movie_id, synopsis_id)
        # You can add additional assertions here to check the database state

    # Add more test cases for the other methods as needed

