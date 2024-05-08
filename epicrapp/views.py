from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Movie, Genre
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import MovieForm, SignUpForm, LoginForm

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