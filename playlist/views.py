from django.shortcuts import render
from .models import MoodEntry
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .spotify_utils import get_spotify_tracks_by_mood
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


MOOD_TO_GENRE = {
    "happy": ["Happy Vibes - Song 1", "Upbeat Pop - Song 2"],
    "sad": ["Soft Piano - Song 3", "Mellow Acoustic - Song 4"],
    "calm": ["Lo-Fi Chill - Song 5", "Ambient Relax - Song 6"],
    "angry": ["Hard Rock - Song 7", "Metal Pulse - Song 8"],
    "excited": ["Dance Beats - Song 9", "Electro Mix - Song 10"],
}

@login_required
def mood_input(request):
    if request.method == 'POST':
        mood = request.POST.get('mood').lower()
        language = request.POST.get('language').lower()
        MoodEntry.objects.create(user=request.user, mood=mood)

        recommendations = get_spotify_tracks_by_mood(mood, language)
        return render(request, 'playlist/recommendations.html', {
            'mood': mood,
            'language': language,
            'recommendations': recommendations
        })

    return render(request, 'playlist/mood_input.html')

@login_required
def mood_history(request):
    entries = MoodEntry.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'playlist/mood_history.html', {'entries': entries})

def landing(request):
    return render(request, 'playlist/landing.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'playlist/register.html', {'error': "Passwords do not match."})

        if User.objects.filter(username=username).exists():
            return render(request, 'playlist/register.html', {'error': "Username already taken."})

        if User.objects.filter(email=email).exists():
            return render(request, 'playlist/register.html', {'error': "Email already registered."})

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        return redirect('login')

    return render(request, 'playlist/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('mood_input')  
        else:
            return render(request, 'playlist/login.html', {'error': "Invalid username or password."})

    return render(request, 'playlist/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('landing')

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            return render(request, 'playlist/forgot_password.html', {'error': "Passwords do not match."})

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return redirect('login')
            #render(request, 'playlist/forgot_password.html', {'success': "Password successfully reset!"})
        except User.DoesNotExist:
            return render(request, 'playlist/forgot_password.html', {'error': "User does not exist."})

    return render(request, 'playlist/forgot_password.html')
