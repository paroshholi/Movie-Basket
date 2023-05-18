"""Movie_Basket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
import app1.views as a
from django.conf import settings
from django.conf.urls.static import static

from app1.views import custom_500_view

handler500 = custom_500_view
urlpatterns = [
    path('',a.home),
    path("movie/<int:movie_id>/", a.movie_details, name="movie_details"),
    path('movies/language/<str:language_code>/', a.movies_by_language, name='movies_by_language'),
    path('movies/genre/<int:genre_id>/', a.movies_by_genre, name='movies_by_genre'),
    path('cast/<int:cast_id>/', a.cast_details, name='cast_details'),
    path('director/<int:director_id>/', a.director_details, name='director_details'),
    path('enter/',include('enter.urls')),
    path('search/', a.search, name='search'),
    path('enter/', include('enter.urls')),
    re_path('.*', a.home),  # catch-all pattern
    path('admin/', admin.site.urls),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
