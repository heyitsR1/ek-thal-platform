from django.shortcuts import render, redirect, get_object_or_404
from .models import FoodListing, Profile, ClaimedListing, Rating
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
    return render(request, 'index.html')
def about(request):
    return render(request, 'about.html')
def signup(request):
    return render(request, 'signup.html')

def contact(request):
    return render(request, 'contact.html')
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

class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'password_reset_done.html'

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

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

@login_required
def food_listing_form(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        title = request.POST.get('title')
        location = request.POST.get('location')
        try:
            quantity = float(request.POST.get('quantity'))
        except (TypeError, ValueError):
            quantity = None
        type_of_food = request.POST.get('type_of_food')
        description = request.POST.get('description')
        prepared_at = request.POST.get('prepared_at')
        image = request.FILES.get('image')
        phone_number_1 = request.POST.get('phone_number_1')
        phone_number_2 = request.POST.get('phone_number_2')
        recurring = request.POST.get('recurring') == 'on'
        storage = request.POST.get('storage')
        prepared_by = request.POST.get('prepared_by')
        special_instructions = request.POST.get('special_instructions')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        try:
            latitude = float(latitude) if latitude else None
            longitude = float(longitude) if longitude else None
        except (TypeError, ValueError):
            latitude = None
            longitude = None
        # Save phone numbers to profile
        profile.phone_number_1 = phone_number_1
        profile.phone_number_2 = phone_number_2
        profile.save()
        try:
            prepared_at_dt = datetime.datetime.strptime(prepared_at, '%Y-%m-%dT%H:%M')
        except Exception:
            prepared_at_dt = None
        # Create listing as pending approval
        listing = FoodListing.objects.create(
            donor=profile,
            title=title,
            location=location,
            quantity=quantity,
            type_of_food=type_of_food,
            description=description,
            prepared_at=prepared_at_dt,
            image=image,
            recurring=recurring,
            storage=storage,
            prepared_by=prepared_by,
            special_instructions=special_instructions,
            status='pending',
            latitude=latitude,
            longitude=longitude,
        )
        # Send email to admin
        try:
            send_mail(
                subject='New Food Listing Pending Approval',
                message=f'A new food listing has been submitted by {profile.user.username}.\n\nTitle: {title}\nLocation: {location}\nQuantity: {quantity} kg\nType: {type_of_food}\nDescription: {description}\nReview: http://127.0.0.1:8000/admin/approve-listing/{listing.id}/',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[a[1] for a in settings.ADMINS],
                fail_silently=True,
            )
        except Exception:
            pass
        return redirect('thank_you')
    # Prefill form fields
    return render(request, 'food_listing_form.html', {'profile': profile})

# Thank you page after submission
def thank_you(request):
    return render(request, 'thank_you.html')

def listing_detail(request, listing_id):
    listing = get_object_or_404(FoodListing, id=listing_id)
    is_org = False
    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)
        is_org = user_profile.is_organization
    claimed_ids = set(ClaimedListing.objects.values_list('food_listing_id', flat=True))
    ai_summary = None
    ai_analysis = None
    if listing.ai_report:
        html = listing.ai_report
        summary_start = html.find('<div class="ai-summary"')
        if summary_start != -1:
            summary_end = html.find('</div>', summary_start)
            if summary_end != -1:
                summary_end += len('</div>')
                ai_summary = html[summary_start:summary_end]
                ai_analysis = html[:summary_start] + html[summary_end:]
            else:
                ai_analysis = html
        else:
            ai_analysis = html
    return render(request, 'listing_detail.html', {
        'listing': listing,
        'is_org': is_org,
        'claimed_ids': claimed_ids,
        'ai_summary': ai_summary,
        'ai_analysis': ai_analysis,
    })

def listings(request):
    food_type = request.GET.get('type_of_food', '')
    location = request.GET.get('location', '')
    listings = FoodListing.objects.filter(status='approved')
    if food_type:
        listings = listings.filter(type_of_food__icontains=food_type)
    if location:
        listings = listings.filter(location__icontains=location)
    listings = listings.order_by('-created_at')
    user_profile = None
    is_org = False
    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)
        is_org = user_profile.is_organization
    return render(request, 'food_listings.html', {
        'listings': listings,
        'food_type': food_type,
        'location': location,
        'is_org': is_org,
    })

@login_required
def claim_listing(request, listing_id):
    profile = Profile.objects.get(user=request.user)
    if not profile.is_organization:
        return redirect('landing_page')
    food_listing = get_object_or_404(FoodListing, id=listing_id)
    # Prevent double-claim
    if ClaimedListing.objects.filter(food_listing=food_listing).exists():
        return redirect('receiver_dashboard')
    ClaimedListing.objects.create(food_listing=food_listing, organization=profile)
    return redirect('receiver_dashboard')

@login_required
def receiver_dashboard(request):
    profile = Profile.objects.get(user=request.user)
    if not profile.is_organization:
        return redirect('landing_page')
    claimed = ClaimedListing.objects.filter(organization=profile).select_related('food_listing').order_by('-claimed_at')
    return render(request, 'receiver_dashboard.html', {'claimed': claimed})

@login_required
def connection_page(request, claimed_listing_id):
    claimed = get_object_or_404(ClaimedListing, id=claimed_listing_id)
    user_profile = Profile.objects.get(user=request.user)
    # Only donor or receiver can access
    if not (user_profile == claimed.food_listing.donor or user_profile == claimed.organization):
        return HttpResponseForbidden("You do not have access to this connection.")
    donor = claimed.food_listing.donor
    receiver = claimed.organization
    listing = claimed.food_listing
    # Determine who is the other party
    if user_profile == donor:
        other = receiver
    else:
        other = donor
    # Check if already rated
    already_rated = Rating.objects.filter(rater=user_profile, claimed_listing=claimed).exists()
    rating_success = False
    if request.method == 'POST' and not already_rated:
        score = int(request.POST.get('score', 0))
        comment = request.POST.get('comment', '')
        if 1 <= score <= 5:
            Rating.objects.create(rater=user_profile, ratee=other, claimed_listing=claimed, score=score, comment=comment)
            rating_success = True
            already_rated = True
    # Get existing rating (if any)
    my_rating = Rating.objects.filter(rater=user_profile, claimed_listing=claimed).first()
    their_rating = Rating.objects.filter(rater=other, claimed_listing=claimed).first()
    return render(request, 'connection_page.html', {
        'claimed': claimed,
        'listing': listing,
        'donor': donor,
        'receiver': receiver,
        'user_profile': user_profile,
        'other': other,
        'already_rated': already_rated,
        'rating_success': rating_success,
        'my_rating': my_rating,
        'their_rating': their_rating,
    })

@staff_member_required
def admin_pending_listings(request):
    pending = FoodListing.objects.filter(status='pending').order_by('-created_at')
    return render(request, 'admin_pending_listings.html', {'pending': pending})

@staff_member_required
def admin_approve_listing(request, listing_id):
    listing = get_object_or_404(FoodListing, id=listing_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            listing.status = 'approved'
        elif action == 'reject':
            listing.status = 'rejected'
        listing.save()
        return redirect('admin_pending_listings')
    return render(request, 'admin_approve_listing.html', {'listing': listing})

def register_individual(request):
    return render(request, 'register_individual.html')

def register_organization(request):
    return render(request, 'register_organization.html')
