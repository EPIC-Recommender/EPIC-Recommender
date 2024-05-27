from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Movie, Genre
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import MovieForm, SignUpForm, LoginForm
import requests
import json 
from django.http import JsonResponse
from django.shortcuts import render
from django.http import JsonResponse
from .models import Movie
from .ai_service import get_similar_movies_from_ai
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def get_similar_movies(request):
    if request.method == "POST":
        selected_movie_id = request.POST.get('movie_id')
        logger.debug(f"Received movie ID: {selected_movie_id}")  # Debugging line
        if selected_movie_id:
            try:
                selected_movie = Movie.objects.get(ID=selected_movie_id)
                logger.debug(f"Selected movie: {selected_movie.title}")  # Debugging line
                recommended_movie_info = get_similar_movies_from_ai(selected_movie)
                return JsonResponse({'movie_info': recommended_movie_info})
            except Movie.DoesNotExist:
                logger.error("Movie not found")
                return JsonResponse({'error': 'Movie not found'}, status=404)
            except Exception as e:
                logger.error(f"Error: {str(e)}")  # Debugging line
                return JsonResponse({'error': 'An error occurred'}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def mainpage(request):
    movies = Movie.objects.all()
    return render(request, 'mainpage.html', {'movies': movies})

def mainpage(request):
    return render(request, 'mainpage.html')

def logout_view(request):
    logout(request)
    return redirect('home') 

class MovieListView(ListView):
    model = Movie
    template_name = 'movies_list.html'
    context_object_name = 'object_list'
    ordering = ['title']  
class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movie_detail.html'  
    
def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movie_list.html', {'movies': movies})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'movie_detail.html', {'movie': movie})

def mainpage(request):
    genres = Genre.objects.all()
    movies = Movie.objects.all()
    return render(request, 'mainpage.html', {'genres': genres, 'movies': movies})

def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm()
    return render(request, 'movie_form.html', {'form': form})

def edit_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_detail', pk=pk)  
    else:
        form = MovieForm(instance=movie)
    return render(request, 'edit_movie.html', {'form': form, 'movie': movie})



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')  # Redirect to home page after signup
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page after login
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home') 

def mainpage(request):
    movies = Movie.objects.all()
    genres = Genre.objects.all()
    
    # Calculate the average rating for each movie
    for movie in movies:
        avg_rating = movie.average_rating()
        movie.avg_rating = avg_rating if avg_rating is not None else 0  # Set a default value for None ratings

    # Fetch top 15 movies of all time based on average rating
    top_movies_all_time = sorted(movies, key=lambda x: x.avg_rating, reverse=True)[:15]

    # Fetch top 15 movies of the current year based on average rating
    current_year = datetime.now().year
    top_movies_year = sorted(
        [movie for movie in movies if movie.release_year == current_year and movie.release_year is not None],
        key=lambda x: x.avg_rating,
        reverse=True
    )[:15]

    # Fetch last 15 added movies
    last_added_movies = Movie.objects.order_by('-created_at')[:15]

    context = {
        'top_movies_all_time': top_movies_all_time,
        'top_movies_year': top_movies_year,
        'last_added_movies': last_added_movies,
        'genres': genres,
        'movies': movies,
    }
    return render(request, 'mainpage.html', context)
    

""" def get_similar_movies(request):
    if request.method == "POST":
        selected_movie_id = request.POST.get('movie_id')
        print(f"Received movie ID: {selected_movie_id}")  # Debugging line
        if selected_movie_id:
            try:
                selected_movie = Movie.objects.get(ID=selected_movie_id)
                print(f"Selected movie: {selected_movie.title}")  # Debugging line
                similar_movies = get_similar_movies_from_ai(selected_movie)
                movie_list = [{
                    "title": movie.title,
                    "imdb_rating": movie.imdb_rating,
                    "rotten_rating": movie.rotten_rating,
                    "meta_rating": movie.meta_rating,
                    "pg_rating": movie.pg_rating
                } for movie in similar_movies]
                return JsonResponse({'movies': movie_list})
            except Movie.DoesNotExist:
                return JsonResponse({'error': 'Movie not found'}, status=404)
            except Exception as e:
                print(f"Error: {str(e)}")  # Debugging line
                return JsonResponse({'error': 'An error occurred'}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400) """
    
    