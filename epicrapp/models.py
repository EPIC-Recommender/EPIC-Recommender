from django.db import models

class Movie(models.Model):
    ID = models.AutoField(primary_key=True, db_column='ID')
    title = models.CharField(max_length=20, db_column='Title')
    imdb_rating = models.IntegerField(db_column='imdb_rating')
    rotten_rating = models.IntegerField(db_column='rotten_rating')
    meta_rating = models.IntegerField(db_column='meta_rating')
    pg_rating = models.CharField(max_length=10, db_column='pg_rating')
    
    
    class Meta:
        db_table = 'movie'

    def __str__(self):
        return self.title
    
class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'genre'

    def __str__(self):
        return self.genre_name