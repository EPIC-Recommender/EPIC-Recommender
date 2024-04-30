from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Movie
from django.shortcuts import render, get_object_or_404

def mainpage(request):
    return render(request, 'mainpage.html')

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