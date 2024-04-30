from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainpage),
    path('movies/', views.MovieListView.as_view(), name='movie_list'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
]
