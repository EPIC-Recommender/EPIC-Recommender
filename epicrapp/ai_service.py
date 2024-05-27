import openai
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI API key
api_key = os.getenv("OPENAI_KEY")
openai.api_key = api_key

# Set up logger
logger = logging.getLogger(__name__)

def get_similar_movies_from_ai(selected_movie):
    try:
        # Prepare input for API request
        input_messages = [
            {"role": "system", "content": f"Selected movie: {selected_movie.title}"},
            {"role": "user", "content": f"IMDB Rating: {selected_movie.imdb_rating}, Rotten Tomatoes Rating: {selected_movie.rotten_rating}, Meta Rating: {selected_movie.meta_rating}, PG Rating: {selected_movie.pg_rating}"},
            {"role": "user", "content": "Recommend a similar movie with detailed information."},
        ]

        # Call the API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=input_messages
        )

        # Extract recommended movie details from response
        recommended_movie_info = response['choices'][0]['message']['content']

        return recommended_movie_info

    except Exception as e:
        # Log the error for debugging
        logger.error(f"OpenAI API call failed: {str(e)}")
        raise








""" import openai
import os
from dotenv import load_dotenv
from .models import Movie

load_dotenv()

api_key = os.getenv("OPENAI_KEY")
openai.api_key = api_key

def get_similar_movies_from_ai(selected_movie):
    movies = Movie.objects.all()

    # Prepare input for API request
    input_messages = [
        {"role": "system", "content": f"Selected movie: {selected_movie.title}"},
        {"role": "user", "content": "Recommend 1 movie similar to the selected movie."},
    ]

    # Call the API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=input_messages
    )

    # Extract recommended movie title from response
    recommended_title = response['choices'][0]['message']['content']

    # Extract the movie title from the response
    # The response format seems consistent, so we can directly extract the title
    start_index = recommended_title.find('"') + 1
    end_index = recommended_title.find('"', start_index)
    recommended_movie_title = recommended_title[start_index:end_index]

    # Filter recommended movies based on title
    recommended_movies = Movie.objects.filter(title=recommended_movie_title.strip())

    return recommended_movies
 """
 