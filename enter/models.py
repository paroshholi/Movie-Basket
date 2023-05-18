from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_language = models.CharField(max_length=100)
    selected_movies = models.ManyToManyField('SelectedMovie')

class SelectedMovie(models.Model):
    movie_id = models.IntegerField()
