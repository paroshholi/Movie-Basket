from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from . import views as enter_views
import requests

# Create your views here.
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

def signup(request):
    if request.method == 'POST':
        # Get user data from the signup form
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email= request.POST['email'] 
        language = request.POST.get('favorite_language', 'English') # Use 'English' as the default if no value is provided

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'username taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email taken')
                return redirect('signup')       
            else:
                # Save user data to session
                request.session['first_name'] = first_name
                request.session['last_name'] = last_name
                request.session['username'] = username
                request.session['password'] = password1
                request.session['email'] = email
                request.session['language'] = language

                # Redirect to the movie selection page
                return redirect('select')
        else:
            messages.info(request,'password not matching')
            return redirect('signup')

    return render(request, 'signup.html')



def confirm_signup(request):
    if request.method == 'POST':
        # Create user object and save to database
        first_name = request.session.get('first_name')
        last_name = request.session.get('last_name')
        username = request.session.get('username')
        password = request.session.get('password')
        email = request.session.get('email')
        favorite_movies = request.session.get('favorite_movies')
        language = request.session.get('language')

        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        user.save()

        # Add favorite language to user profile
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.favorite_language = language
        user_profile.selected_movies.clear()
        for movie_id in favorite_movies:
            user_profile.selected_movies.create(movie_id=movie_id)
        user_profile.save()
        return redirect('/')
    else:
        first_name = request.session.get('first_name')
        last_name = request.session.get('last_name')
        email = request.session.get('email')
        favorite_movies = request.session.get('favorite_movies')
        language = request.session.get('language')

        movies = favorite_movies
        return render(request, 'confirm_signup.html', {'first_name': first_name, 'last_name': last_name, 'email': email, 'movies': movies, 'language': language})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'inavalid credentials')
            return redirect('login')
    else:
        return render(request,'login.html')
    

def logout(request):
    auth.logout(request)
    return redirect('/')

def select(request):
    languages = ['te','ta','en', 'hi','ja']  # English, Telugu, Tamil, Hindi, Japanese
    movies=[]
    for lang in languages:
        url = f"https://api.themoviedb.org/3/discover/movie?with_original_language={lang}&api_key=816c581d9313e9dd0de3ffbef8993179"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        movies = movies + data['results'][:6]

    if request.method == 'POST':
        selected_movies = request.POST.getlist('selected_movies')
        # Save selected movies to session
        request.session['favorite_movies'] = selected_movies

        # Redirect to the confirm signup page
        return redirect('confirm_signup')


    context = { 'movies': movies}
    return render(request, 'top_movies.html', context)

from django.shortcuts import redirect

def handle_enter_url(request, remaining_url):
    # Extract the segments from the remaining URL
    segments = remaining_url.split('/')

    # Define a mapping of segment to corresponding view
    view_mapping = {
        'signup': signup,
        'login': login,
        'logout': logout,
        'select': select,
        'confirm_signup': confirm_signup,
        # Add more mappings as needed
    }

    # Iterate through the segments and find the corresponding view
    current_view = enter_views  # Set initial view as enter_views module
    for segment in segments:
        if segment in view_mapping:
            current_view = view_mapping[segment]
        else:
            # Handle case where segment does not match any view
            return redirect('home')  # Redirect to home or any appropriate page

    # Call the final view with the remaining URL segments
    return current_view(request)

# Add your existing signup, login, logout, select, confirm_signup views here
# ...
