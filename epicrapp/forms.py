from django import forms
from .models import Movie
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'imdb_rating', 'rotten_rating', 'meta_rating', 'pg_rating']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'imdb_rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'rotten_rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'meta_rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'pg_rating': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']  # Add more fields as needed

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']