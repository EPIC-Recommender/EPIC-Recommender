import openai
import os
from dotenv import load_dotenv
from .models import Movie

load_dotenv()

api_key = os.getenv("OPENAI_KEY")

openai.api_key = api_key

def get_similar_movies_from_ai(selected_movie):
    movies = Movie.objects.all()
    movie_data = [
        {
            "title": movie.title,
            "imdb_rating": movie.imdb_rating,
            "rotten_rating": movie.rotten_rating,
            "meta_rating": movie.meta_rating,
            "pg_rating": movie.pg_rating,
        }
        for movie in movies
    ]

    prompt = f"""
    You are a movie recommendation engine. Given a selected movie and a list of other movies, recommend 5 movies that are similar to the selected movie based on ratings and title.
    Selected movie: {selected_movie.title} (IMDB Rating: {selected_movie.imdb_rating})
    Other movies: {movie_data}
    Recommended movies (titles only):
    """

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )

    recommended_titles = response.choices[0].text.strip().split('\n')
    recommended_movies = Movie.objects.filter(title__in=recommended_titles)
    
    return recommended_movies
