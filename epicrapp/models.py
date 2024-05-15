from django.db import models
from django.contrib.auth.models import AbstractUser , Permission , Group

class CustomUser(AbstractUser):
    # Add any additional fields here
    age = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        permissions = (("view_user", "Can view user"),)

    # Override the groups field
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
    )

    # Override the user_permissions field
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
    )

class Movie(models.Model):
    ID = models.AutoField(primary_key=True, db_column='ID')
    title = models.CharField(max_length=20, db_column='Title')
    imdb_rating = models.IntegerField(db_column='imdb_rating')
    rotten_rating = models.IntegerField(db_column='rotten_rating')
    meta_rating = models.IntegerField(db_column='meta_rating')
    pg_rating = models.CharField(max_length=10, db_column='pg_rating') 
    release_year = models.IntegerField(null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def average_rating(self):
        ratings = [self.imdb_rating, self.meta_rating, self.pg_rating, self.rotten_rating]
        numeric_ratings = [float(rating) for rating in ratings if rating is not None]  # Convert to float and handle None values
        if numeric_ratings:  # Check if the list is not empty
            return sum(numeric_ratings) / len(numeric_ratings)
        return None  # Handle the case where all ratings might be None
    
    class Meta:
        db_table = 'movie'

    def __str__(self):
        return self.title
    
class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.CharField()

    class Meta:
        managed = False
        db_table = 'genre'

    def __str__(self):
        return self.genre_name
    
    
    
class MovieActor(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey('Person', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('movie', 'actor')

class MovieAward(models.Model):
    award = models.ForeignKey('Award', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

class MovieDirector(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    director = models.ForeignKey('Person', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('movie', 'director')

class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('movie', 'genre')

class MovieProducer(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    producer = models.ForeignKey('Person', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('movie', 'producer')

class MovieSynopsis(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE)
    synopsis = models.ForeignKey('Synopsis', on_delete=models.CASCADE)

class Person(models.Model):
    ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    gender = models.BooleanField(null=True)
    nationality = models.CharField(max_length=255, null=True)
    DOB = models.DateField(null=True)

    def __str__(self):
        return self.name

class Synopsis(models.Model):
    ID = models.AutoField(primary_key=True)
    synopsis = models.TextField()

    def __str__(self):
        return self.synopsis

class Award(models.Model):
    ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return self.name
