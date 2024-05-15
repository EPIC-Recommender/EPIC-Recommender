from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Movie, Genre
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import MovieForm, SignUpForm, LoginForm
from . config import AI_API_KEY
import requests
import json 
from django.http import JsonResponse
from datetime import datetime

def main(request):
    movies = Movie.objects.all()  # Retrieve all movies from the database
    return render(request, 'main.html', {'movies': movies})

def get_recommendations(request):
    if request.method == 'POST':
        selected_movie_id = request.POST.get('selected_movie_id')
        
        # Retrieve the selected movie object after obtaining its ID
        selected_movie = Movie.objects.get(ID=selected_movie_id)  # Use 'ID' instead of 'id'
        
        # Gather all movie information including genres
        all_movies_data = []
        for movie in Movie.objects.all():
            # Retrieve genres associated with the current movie
           # genres = Genre.objects.filter(moviegenre__movie=movie)
            #genre_names = [genre.genre_name for genre in genres]
            all_movies_data.append({
                'title': movie.title,
             #   'genres': genre_names,
                'imdb_rating': movie.imdb_rating,
                'rotten_rating': movie.rotten_rating,
                'meta_rating': movie.meta_rating
            })
        
        # Send movie data to AI service
        ai_url = 'https://api.openai.com'
        headers = {'Authorization': 'Bearer ' + AI_API_KEY, 'Content-Type': 'application/json'}
        data = {'selected_movie': selected_movie.__dict__, 'all_movies': all_movies_data}
        
        # Serialize the selected movie object to dictionary
        selected_movie_data = {
            'title': selected_movie.title,
          #  'genres': [genre.genre_name for genre in selected_movie.genres.all()],
            'imdb_rating': selected_movie.imdb_rating,
            'rotten_rating': selected_movie.rotten_rating,
            'meta_rating': selected_movie.meta_rating
        }
        
        # Update data with selected movie data
        data['selected_movie'] = selected_movie_data
        
        # Send the request to the AI service
        response = requests.post(ai_url, headers=headers, json=data)  # Use json parameter to automatically serialize data
        
        if response.status_code == 200:
            recommendations = response.json()
            return JsonResponse({'recommendations': recommendations})
        else:
            return JsonResponse({'error': 'Failed to get recommendations from AI service'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def get_similar_movies(selected_movie_id):
    selected_movie = Movie.objects.get(id=selected_movie_id)
    # Placeholder logic to fetch similar movies based on selected_movie
    similar_movies = Movie.objects.filter( imdb_rating__gte=selected_movie.imdb_rating - 0.5, imdb_rating__lte=selected_movie.imdb_rating + 0.5).exclude(id=selected_movie.id)[:5]  # Fixed filter conditions
    return similar_movies

def mainpage(request):
    # Assuming movie_id is obtained from the request
    movie_id = request.GET.get('movie_id')
    similar_movies = get_similar_movies(movie_id)
    return render(request, 'mainpage.html', {'similar_movies': similar_movies})


def mainpage(request):
    return render(request, 'mainpage.html')

def logout_view(request):
    logout(request)
    return redirect('home') 

class MovieListView(ListView):
    model = Movie
    template_name = 'movies_list.html'  
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

def mainpage(request):
    movies = Movie.objects.all()

    # Calculate the average rating for each movie
    for movie in movies:
        movie.avg_rating = movie.average_rating()

    # Fetch top 15 movies of all time based on average rating
    top_movies_all_time = sorted(movies, key=lambda x: x.avg_rating, reverse=True)[:15]

    # Fetch top 15 movies of the current year based on average rating
    current_year = datetime.now().year
    top_movies_year = sorted(
        [movie for movie in movies if movie.release_year == current_year],
        key=lambda x: x.avg_rating,
        reverse=True
    )[:15]

    # Fetch last 15 added movies
    last_added_movies = Movie.objects.order_by('-created_at')[:15]

    context = {
        'top_movies_all_time': top_movies_all_time,
        'top_movies_year': top_movies_year,
        'last_added_movies': last_added_movies,
    }
    return render(request, 'mainpage.html', context)
