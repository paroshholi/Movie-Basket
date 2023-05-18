from django.shortcuts import render
from .models import smovie
from enter.models import UserProfile
import requests
import json
# Create your views here.
def home(request):
    a = smovie.objects.all()[:6]
    trending_movies = get_trending_movies()
    top_rated_movies = get_top_rated_movies()

    
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get user's favorite language from their profile
        user = request.user
        favorite_language = user.userprofile.favorite_language
        
        # Get movies in user's favorite language
        lan_movies = get_movies_by_language(request)
        recommended_movies = get_recommended_movies(request)
    else:
        # Generate 6 English movies if user is not authenticated
        favorite_language = "en"
        lan_movies = get_movies_by_default(request, language="en")
        recommended_movies = {}
    if favorite_language == 'en':
        lan='English'
    elif favorite_language == 'te':
        lan='Telugu'
    elif favorite_language == 'ta':
        lan='Tamil'  
    elif favorite_language == 'hi':
        lan='Hindi'   
    context = {
        "trending_movies": trending_movies,
        "top_rated_movies": top_rated_movies,
        "lan_movies": lan_movies,
        "lan" : lan,
        "recommended_movies" : recommended_movies,
        "data": a
    }
    return render(request, "home.html", context)



def get_trending_movies():
    url = "https://api.themoviedb.org/3/trending/all/week?api_key=816c581d9313e9dd0de3ffbef8993179"
    response = requests.get(url)
    data = json.loads(response.text)
    return data["results"][:6]


def movie_details(request, movie_id):
    # Get movie details
    movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=816c581d9313e9dd0de3ffbef8993179&language=en-US"
    movie_response = requests.get(movie_url)
    movie = movie_response.json()

    # Get credits details
    credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=816c581d9313e9dd0de3ffbef8993179&language=en-US"
    credits_response = requests.get(credits_url)
    credits = credits_response.json()
    # Retrieve watch providers for India
    providers_url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key=816c581d9313e9dd0de3ffbef8993179&language=en-US&country=IN"
    providers_response = requests.get(providers_url)
    watch_providers = providers_response.json().get("results", {}).get("IN", {}).get("flatrate", [])

    # Define a dictionary to map OTT platform IDs to their respective links
    ott_links = {
        8: "https://www.netflix.com/",
        119: "https://www.primevideo.com/",
        337: "https://www.disneyplus.com/",
        122: "https://www.hotstar.com/",
        232: "https://www.zee5.com/",
        237: "https://www.sonyliv.com/",
        220: "https://www.jiocinema.com/",
        121: "https://www.voot.com/",
        192: "https://www.youtube.com/",
        309: "https://www.sunnxt.com/",
        532: "https://www.aha.video/",
        350: "https://www.apple.com/in/apple-tv-plus/",
        2:   "https://tv.apple.com/",
        437: "https://www.hungama.com/tv-shows/",
        218: "https://erosnow.com/tv",
        515: "https://www.mxplayer.in/",
        1898:"https://www.amazon.in/minitv"
    }

    # Add link to the providers
    for provider in watch_providers:
        provider_id = provider.get("provider_id")
        provider["link"] = ott_links.get(provider_id, "")
        print(provider["link"])

    # Add logo path to the providers
    for provider in watch_providers:
        provider["logo_path"] = f"https://image.tmdb.org/t/p/original{provider.get('logo_path', '')}"


    # Extract director from credits
    director = ""
    for crew in credits["crew"]:
        if crew["job"] == "Director":
            director = crew["name"]
            break

    # Add crew details to movie dictionary
    movie["director"] = {
        "id": crew["id"],
        "name": crew["name"]
    }
    movie["credits"] = credits["cast"]
    # Calculate average rating
    vote_average = movie["vote_average"]
    vote_count = movie["vote_count"]
    if vote_count > 0:
        rating_percentage = (vote_average / 10) * 100
        rating_average = round(vote_average, 1)
    else:
        rating_percentage = 0
        rating_average = 0
    # Retrieve reviews for the current movie
    reviews_url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key=816c581d9313e9dd0de3ffbef8993179&language=en-US&page=1"
    reviews_response = requests.get(reviews_url)
    reviews_data = reviews_response.json()
    reviews = reviews_data["results"]

    context = {
        "movie": movie,
        "reviews": reviews,
        "watch_providers": watch_providers,
        "rating_percentage": rating_percentage,
        "rating_average": rating_average,
    }

    return render(request, "movie.html", context)

def search(request):
    query = request.POST.get('query', '')
    movie_url = f'https://api.themoviedb.org/3/search/movie?query={query}&api_key=816c581d9313e9dd0de3ffbef8993179'
    movie_response = requests.get(movie_url)
    movies = movie_response.json().get('results', [])

    cast_url = f'https://api.themoviedb.org/3/search/person?query={query}&api_key=816c581d9313e9dd0de3ffbef8993179'
    cast_response = requests.get(cast_url)
    cast = cast_response.json().get('results', [])

    context = {
        'query': query,
        'movies': movies,
        'cast': cast,
    }
    return render(request, 'results.html', context)


def movies_by_language(request, language_code):
    url = f'https://api.themoviedb.org/3/discover/movie?with_original_language={language_code}&api_key=816c581d9313e9dd0de3ffbef8993179'
    response = requests.get(url)
    movies = response.json().get('results', [])
    if language_code == 'en':
        lan='English'
    elif language_code == 'te':
        lan='Telugu'
    elif language_code == 'ta':
        lan='Tamil'  
    elif language_code == 'hi':
        lan='Hindi' 
    elif language_code == 'ml':
        lan='Malyalam' 
    elif language_code == 'es':
        lan='Spanish' 
    elif language_code == 'ja':
        lan='Japaneese' 
    elif language_code == 'ko':
        lan='korean' 
    context = {
        'movies': movies,
        'language_code': lan
    }
    return render(request, 'movies_by_language.html', context)


def movies_by_genre(request, genre_id):
    url = f"https://api.themoviedb.org/3/discover/movie?api_key=816c581d9313e9dd0de3ffbef8993179&with_genres={genre_id}"
    response = requests.get(url)
    data = response.json()
    movies = data["results"]
    return render(request, "movies_by_genre.html", {"movies": movies})

def get_top_rated_movies():
    url = "https://api.themoviedb.org/3/movie/top_rated?api_key=816c581d9313e9dd0de3ffbef8993179"
    response = requests.get(url)
    data = response.json()
    return data["results"][:6]
def director_details(request, director_id):
    url = f"https://api.themoviedb.org/3/person/{director_id}?api_key=816c581d9313e9dd0de3ffbef8993179&language=en-US"
    response = requests.get(url)
    data = response.json()
    
    # Get director details
    director_name = data['name']
    director_biography = data['biography']
    director_profile_path = data['profile_path']
    
    # Get movies directed by the director
    url = f"https://api.themoviedb.org/3/person/{director_id}/movie_credits?api_key=816c581d9313e9dd0de3ffbef8993179&language=en-US"
    response = requests.get(url)
    data = response.json()
    
    movie_credits = []
    for credit in data['crew']:
        if credit['job'] == "Director":
            movie_credits.append({
                "id": credit['id'],
                "title": credit['title'],
                "poster_path": credit['poster_path']
            })
    
    context = {
        'director_name': director_name,
        'director_biography': director_biography,
        'director_profile_path': director_profile_path,
        'movie_credits': movie_credits
    }
    
    return render(request, 'director_details.html', context)
def cast_details(request, cast_id):
    url = f"https://api.themoviedb.org/3/person/{cast_id}?api_key=816c581d9313e9dd0de3ffbef8993179&language=en-US"
    response = requests.get(url)
    cast = response.json()

    url = f"https://api.themoviedb.org/3/person/{cast_id}/movie_credits?api_key=816c581d9313e9dd0de3ffbef8993179&language=en-US"
    response = requests.get(url)
    credits = response.json()

    return render(request, "cast.html", {"cast": cast, "credits": credits})


def get_movies_by_language(request):
    # Get user's favorite language from their profile
    user = request.user
    favorite_language = user.userprofile.favorite_language
    # Make API request to TMDb to get top 6 movies in user's favorite language
    url = f"https://api.themoviedb.org/3/discover/movie?with_original_language={favorite_language}&api_key=816c581d9313e9dd0de3ffbef8993179"


    # Extract movie data from API response
    response = requests.get(url)
    data = json.loads(response.text)
    return data["results"][:6]

def get_movies_by_default(request, language="en"):
    # Make API request to TMDb to get top 6 movies in specified language
    url = f"https://api.themoviedb.org/3/discover/movie?with_original_language={language}&api_key=816c581d9313e9dd0de3ffbef8993179"
    response = requests.get(url)
    data = json.loads(response.text)
    return data["results"][:6]

def get_recommended_movies(request):
    # Get user's favorite language from their profile
    user = request.user
    selected_movies = user.userprofile.selected_movies.all().values_list('movie_id', flat=True)
    movie_id = selected_movies[0]
    # Make API request to TMDb to get top 6 movies in user's favorite language
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key=816c581d9313e9dd0de3ffbef8993179"

    # Extract movie data from API response
    response = requests.get(url)
    data = json.loads(response.text)
    return data["results"][:6]

def custom_500_view(request):
    return render(request, '500.html', status=500)