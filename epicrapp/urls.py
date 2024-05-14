from django.urls import path
from . import views
from .views import signup, login_view, logout_view

urlpatterns = [
    path('', views.mainpage, name='home'),
    path('movies/', views.MovieListView.as_view(), name='movie_list'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('edit_movie/<int:pk>/', views.edit_movie, name='edit_movie'),
    path('get_recommendations/', views.get_recommendations, name='get_recommendations'),

]
