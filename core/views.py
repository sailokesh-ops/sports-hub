import requests
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import FavoriteTeam

def home(request):
    return render(request, 'home.html',{'is_home':True})

def live_scores(request):
    url = "https://api.cricapi.com/v1/currentMatches?apikey=7de296be-2141-49e1-9a4b-c21c3f9db4d1&offset=0"

    response = requests.get(url)
    data = response.json()

    matches = []

    for match in data.get("data", []):
        teams = match.get("teams", [])

        matches.append({
            'team1': teams[0] if len(teams) > 0 else "Team A",
            'team2': teams[1] if len(teams) > 1 else "Team B",
            'score': "Live",
            'status': match.get("status", "Live")
        })

    if not matches:
        matches = [{
            "team1": "No Live Matches",
            "team2": "",
            "score": "",
            "status": "Check again later ⏳"
        }]

    return render(request, 'live_scores.html', {'matches': matches})

def fixtures(request):
    url = "https://api.cricapi.com/v1/matches?apikey=7de296be-2141-49e1-9a4b-c21c3f9db4d1&offset=0"

    response = requests.get(url)
    data = response.json()

    matches = []

    for match in data.get("data", []):
        teams = match.get("teams", [])

        matches.append({
            'team1': teams[0] if len(teams) > 0 else "Team A",
            'team2': teams[1] if len(teams) > 1 else "Team B",
            'status': match.get("status", "Upcoming")
        })

    if not matches:
        matches = [
            {'team1': 'India', 'team2': 'England', 'status': 'Tomorrow 7 PM'},
            {'team1': 'Barcelona', 'team2': 'Atletico', 'status': 'Today 10 PM'}
        ]

    return render(request, 'fixtures.html', {'matches': matches})

def news(request):
    url = "https://newsapi.org/v2/top-headlines?category=sports&apiKey=007871b8fe2c41df91222586c7e0e01a"
    
    response=requests.get(url)
    data=response.json()

    articles = []

    for article in data.get("articles", [])[:20]:
        articles.append({
            'title': article.get('title'),
            'description': article.get('description'),
            'image': article.get('urlToImage') or 'https://via.placeholder.com/300'
        })
    title = article.get('title', '')
    team = 'India' if 'India' in title else 'Other'

    return render(request, 'news.html', {'articles': articles})

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('/')

    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('/')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def add_favorite(request):
    if request.method == 'POST':
        team = request.POST['team']

        FavoriteTeam.objects.create(
            user=request.user,
            team_name=team
        )

        return redirect('/favorites/')

    return render(request, 'add_favorite.html')

@login_required
def favorites(request):
    teams = FavoriteTeam.objects.filter(user=request.user)
    return render(request, 'favorites.html', {'teams': teams})

def reels(request):
    videos = [
          'videos/video1.mp4',
          'videos/video2.mp4',
          'videos/video3.mp4',
          'videos/video4.mp4',
          'videos/video5.mp4',

    ]

    return render(request, 'reels.html', {'videos': videos})