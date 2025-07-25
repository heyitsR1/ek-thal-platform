from django.shortcuts import render, redirect, get_object_or_404
# from .models import FoodListing, Profile, ClaimedListing, Rating
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.db.models import Q
# from .utils import analyze_food_listing_with_gemini
from django.http import HttpResponseForbidden
import datetime
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.conf import settings



# Create your views here.

def home(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

@csrf_protect
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        phone_number_1 = request.POST.get('phone_number_1')
        phone_number_2 = request.POST.get('phone_number_2')
        is_organization = request.POST.get('is_organization') == 'on'
        if not (username and password and password2 and email and phone_number_1 and phone_number_2):
            return render(request, 'register.html', {'error': 'All fields are required.'})
        if password != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match.'})
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists.'})
        user = User.objects.create_user(username=username, password=password, email=email)
        Profile.objects.create(user=user, phone_number_1=phone_number_1, phone_number_2=phone_number_2, is_organization=is_organization)
        return render(request, 'register.html', {'success': True})
    return render(request, 'register.html')


@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Ensure Profile exists for this user
            try:
                profile = Profile.objects.get(user=user)
            except Profile.DoesNotExist:
                profile = Profile.objects.create(user=user, phone_number_1='', phone_number_2='', is_organization=False)
            if profile.is_organization:
                return redirect('listings')
            else:
                return redirect('food_listing_form')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials.'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('landing_page')