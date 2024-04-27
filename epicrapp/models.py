from django.db import models

class Movie(models.Model):
    ID = models.AutoField(primary_key=True, db_column='ID')
    title = models.CharField(max_length=20, db_column='Title')
    movieawards = models.IntegerField(db_column='movei_awards')
    imdb_rating = models.IntegerField(db_column='imdb_rating')
    rotten_rating = models.IntegerField(db_column='rotten_rating')
    meta_rating = models.IntegerField(db_column='meta_rating')
    pg_rating = models.CharField(max_length=10, db_column='pg_rating')
    genre = models.CharField(max_length=50, db_column='genre')
    
    class Meta:
        db_table = 'movie'

    def __str__(self):
        return self.title
    
