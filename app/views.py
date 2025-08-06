from django.shortcuts import render, redirect, get_object_or_404
from .models import FoodListing, Profile, ClaimedListing, Rating, Certificate
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.db.models import Q
# from .utils import analyze_food_listing_with_gemini
from django.http import HttpResponseForbidden, HttpResponse
import datetime
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.conf import settings
import math
from .email_notifications import email_notifier
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
import os
from PIL import Image as PILImage, ImageDraw, ImageFont
import requests



def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points using the Haversine formula.
    Returns distance in kilometers.
    """
    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        return float('inf')
    
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    
    return c * r

def home(request):
    try:
        # Test database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # Check if this is a health check request
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        if 'healthcheck' in user_agent.lower() or 'railway' in user_agent.lower():
            return HttpResponse("OK", content_type="text/plain")
        
        return render(request, 'index.html')
    except Exception as e:
        print(f"Database error in home view: {e}")
        # For health checks, return error status
        if 'healthcheck' in request.META.get('HTTP_USER_AGENT', '').lower():
            return HttpResponse(f"ERROR: {str(e)}", content_type="text/plain", status=500)
        return render(request, 'maintenance.html')
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
    try:
        if request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=request.user)
                if profile.is_receiver:
                    return redirect('listings')
                else:
                    return redirect('food_listing_form')
            except Profile.DoesNotExist:
                pass
    except Exception as e:
        print(f"Database error in login view: {e}")
        return render(request, 'maintenance.html')

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
            try:
                profile = Profile.objects.get(user=user)
            except Profile.DoesNotExist:
                profile = Profile.objects.create(user=user, phone_number_1='', phone_number_2='', is_organization=False, is_receiver=False)
            if profile.is_receiver:
                return redirect('listings')
            else:
                return redirect('food_listing_form')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials.'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

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
        
        # Send email notification to admin
        try:
            email_notifier.send_admin_new_listing_notification(listing)
        except Exception as e:
            print(f"Email notification failed: {e}")
        
        # Store the listing ID in session for the thank you page
        request.session['last_donation_id'] = listing.id
        return redirect('thank_you')
    # Prefill form fields
    return render(request, 'food_listing_form.html', {'profile': profile})

# Thank you page after submission
def thank_you(request):
    listing = None
    listing_id = request.session.get('last_donation_id')
    if listing_id:
        try:
            listing = FoodListing.objects.get(id=listing_id)
            # Clear the session data after retrieving it
            del request.session['last_donation_id']
        except FoodListing.DoesNotExist:
            pass
    return render(request, 'thank_you.html', {'listing': listing})

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
    try:
        radius = request.GET.get('radius', '')
        listings = FoodListing.objects.filter(status='approved')
    except Exception as e:
        print(f"Database error in listings view: {e}")
        return render(request, 'maintenance.html')
    
    # Filter by distance if radius is provided and user is authenticated
    if radius and request.user.is_authenticated:
        try:
            radius_km = float(radius)
            user_profile = Profile.objects.get(user=request.user)
            
            if user_profile.latitude and user_profile.longitude:
                # Filter listings within the specified radius
                nearby_listings = []
                for listing in listings:
                    if listing.latitude and listing.longitude:
                        distance = calculate_distance(
                            user_profile.latitude, user_profile.longitude,
                            listing.latitude, listing.longitude
                        )
                        if distance <= radius_km:
                            nearby_listings.append(listing)
                listings = nearby_listings
        except (ValueError, Profile.DoesNotExist):
            pass
    
    listings = sorted(listings, key=lambda x: x.created_at, reverse=True)
    
    user_profile = None
    is_org = False
    if request.user.is_authenticated:
        try:
            user_profile = Profile.objects.get(user=request.user)
            is_org = user_profile.is_organization
        except Profile.DoesNotExist:
            pass
    
    return render(request, 'food_listings.html', {
        'listings': listings,
        'radius': radius,
        'is_org': is_org,
    })

def claim_listing(request, listing_id):
    if not request.user.is_authenticated:
        return redirect('login')
    profile = Profile.objects.get(user=request.user)
    if not profile.is_organization:
        return redirect('landing_page')
    food_listing = get_object_or_404(FoodListing, id=listing_id)
    # Prevent double-claim
    if ClaimedListing.objects.filter(food_listing=food_listing).exists():
        return redirect('receiver_dashboard')
    
    claimed_listing = ClaimedListing.objects.create(food_listing=food_listing, organization=profile)
    
    # Send email notification to donor
    try:
        email_notifier.send_claim_notification_to_donor(claimed_listing)
    except Exception as e:
        print(f"Email claim notification failed: {e}")
    
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
def dashboard_pending_listings(request):
    pending = FoodListing.objects.filter(status='pending').order_by('-created_at')
    return render(request, 'dashboard_pending_listings.html', {'pending': pending})

@staff_member_required
def dashboard_approve_listing(request, listing_id):
    listing = get_object_or_404(FoodListing, id=listing_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            listing.status = 'approved'
            listing.save()
            
            # Send email notifications
            try:
                # Notify donor about approval
                email_notifier.send_donor_listing_approved_notification(listing)
                
                # Notify all receivers about new available food
                receivers_notified = email_notifier.send_receivers_new_listing_notification(listing)
                print(f"Notified {receivers_notified} receivers about new listing")
            except Exception as e:
                print(f"Email notifications failed: {e}")
                
        elif action == 'reject':
            listing.status = 'rejected'
            listing.save()
            
            # Send rejection notification to donor
            try:
                email_notifier.send_donor_listing_rejected_notification(listing)
            except Exception as e:
                print(f"Email rejection notification failed: {e}")
        return redirect('dashboard_pending_listings')
    return render(request, 'dashboard_approve_listing.html', {'listing': listing})

def register_individual(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        phone_number_1 = request.POST.get('phone_number_1')
        phone_number_2 = request.POST.get('phone_number_2')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        try:
            latitude = float(latitude) if latitude else None
            longitude = float(longitude) if longitude else None
        except (TypeError, ValueError):
            latitude = None
            longitude = None
        role = request.POST.get('role')
        is_organization = False
        is_receiver = (role == 'receiver')
        if not (username and password and password2 and email and phone_number_1 and phone_number_2 and role):
            return render(request, 'register_individual.html', {'error': 'All fields are required.'})
        if password != password2:
            return render(request, 'register_individual.html', {'error': 'Passwords do not match.'})
        if User.objects.filter(username=username).exists():
            return render(request, 'register_individual.html', {'error': 'Username already exists.'})
        user = User.objects.create_user(username=username, password=password, email=email)
        Profile.objects.create(user=user, phone_number_1=phone_number_1, phone_number_2=phone_number_2, is_organization=is_organization, is_receiver=is_receiver, latitude=latitude, longitude=longitude)
        return render(request, 'register_individual.html', {'success': True})
    return render(request, 'register_individual.html')

def register_organization(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        phone_number_1 = request.POST.get('phone_number_1')
        phone_number_2 = request.POST.get('phone_number_2')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        try:
            latitude = float(latitude) if latitude else None
            longitude = float(longitude) if longitude else None
        except (TypeError, ValueError):
            latitude = None
            longitude = None
        role = request.POST.get('role')
        is_organization = True
        is_receiver = (role == 'receiver')
        if not (username and password and password2 and email and phone_number_1 and phone_number_2 and role):
            return render(request, 'register_organization.html', {'error': 'All fields are required.'})
        if password != password2:
            return render(request, 'register_organization.html', {'error': 'Passwords do not match.'})
        if User.objects.filter(username=username).exists():
            return render(request, 'register_organization.html', {'error': 'Username already exists.'})
        user = User.objects.create_user(username=username, password=password, email=email)
        Profile.objects.create(user=user, phone_number_1=phone_number_1, phone_number_2=phone_number_2, is_organization=is_organization, is_receiver=is_receiver, latitude=latitude, longitude=longitude)
        return render(request, 'register_organization.html', {'success': True})
    return render(request, 'register_organization.html')

def user_profile_context(request):
    try:
        if request.user.is_authenticated:
            try:
                return {'profile': Profile.objects.get(user=request.user)}
            except Profile.DoesNotExist:
                return {'profile': None}
        return {'profile': None}
    except Exception as e:
        # Log the error but don't crash the app
        print(f"Context processor error: {e}")
        # Return empty context to prevent template errors
        return {'profile': None, 'user': None}

def handler500(request, exception=None):
    """Custom 500 error handler for debugging"""
    import traceback
    import sys
    
    # Log the error details
    exc_type, exc_value, exc_traceback = sys.exc_info()
    error_details = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    
    print(f"500 Error Details: {error_details}")
    
    # Return a simple error response
    return render(request, '500.html', status=500)

def health_check(request):
    """Simple health check endpoint for Railway"""
    try:
        # Test database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
        
        return HttpResponse("OK", content_type="text/plain")
    except Exception as e:
        print(f"Health check failed: {e}")
        return HttpResponse(f"ERROR: {str(e)}", content_type="text/plain", status=500)

def test_csrf(request):
    """Test view to verify CSRF is working"""
    if request.method == 'POST':
        return HttpResponse("CSRF test successful!")
    return render(request, 'test_csrf.html')

def debug_csrf(request):
    """Debug view to check CSRF token status"""
    from django.middleware.csrf import get_token
    
    # Get the CSRF token
    csrf_token = get_token(request)
    
    # Check if token exists in cookies
    csrf_cookie = request.COOKIES.get('csrftoken')
    
    debug_info = {
        'csrf_token': csrf_token,
        'csrf_cookie': csrf_cookie,
        'method': request.method,
        'headers': dict(request.headers),
        'cookies': dict(request.COOKIES),
    }
    
    return HttpResponse(f"<pre>{debug_info}</pre>")

@login_required
def generate_certificate(request, listing_id):
    """Generate a donation certificate for the donor using Canva template"""
    # Get the food listing
    food_listing = get_object_or_404(FoodListing, id=listing_id)
    
    # Check if user is the donor
    if request.user != food_listing.donor.user:
        return HttpResponseForbidden("You can only generate certificates for your own donations.")
    
    # Check if certificate already exists
    certificate, created = Certificate.objects.get_or_create(
        donor=food_listing.donor,
        food_listing=food_listing
    )
    
    try:
        # Load the certificate template
        template_path = os.path.join(settings.BASE_DIR, 'static', 'certificate.png')
        if not os.path.exists(template_path):
            # Fallback to staticfiles directory
            template_path = os.path.join(settings.STATIC_ROOT or settings.STATICFILES_DIRS[0], 'certificate.png')
        
        # Open the template image
        template_img = PILImage.open(template_path)
        
        # Create a copy to work with
        certificate_img = template_img.copy()
        
        # Lighten the background if it's too dark
        # Convert to RGB if needed
        if certificate_img.mode != 'RGB':
            certificate_img = certificate_img.convert('RGB')
        
        # Apply a lightening effect to make the background less dark
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Brightness(certificate_img)
        certificate_img = enhancer.enhance(1.3)  # Increase brightness by 30%
        
        draw = ImageDraw.Draw(certificate_img)
        
        # Try to load Pinyon Script font, fallback to default if not available
        try:
            # Load the Pinyon Script font from static directory
            font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'PinyonScript-Regular.ttf')
            if not os.path.exists(font_path):
                # Fallback to system font
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 48)  # macOS fallback
            else:
                font = ImageFont.truetype(font_path, 48)
        except Exception as font_error:
            print(f"Font loading error: {font_error}")
            # If font loading fails, use default
            font = ImageFont.load_default()
        
        # Get donor name
        donor_name = food_listing.donor.user.get_full_name() or food_listing.donor.user.username
        
        # Calculate text position (center of the image)
        img_width, img_height = certificate_img.size
        text_bbox = draw.textbbox((0, 0), donor_name, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Position text in the center with better spacing
        x = (img_width - text_width) // 2
        y = img_height // 2 - 80  # Move up a bit more for better positioning
        
        # Draw the donor name with the specified color
        donor_color = (166, 123, 38)  # #a67b26 in RGB
        draw.text((x, y), donor_name, font=font, fill=donor_color)
        
        # Add certificate number (smaller font) with more spacing
        try:
            small_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 20)  # Slightly smaller font
        except Exception as small_font_error:
            print(f"Small font loading error: {small_font_error}")
            small_font = ImageFont.load_default()
        
        cert_text = f"Certificate #{certificate.certificate_number}"
        cert_bbox = draw.textbbox((0, 0), cert_text, font=small_font)
        cert_width = cert_bbox[2] - cert_bbox[0]
        cert_x = (img_width - cert_width) // 2
        cert_y = y + text_height + 80  # Much more spacing between name and certificate number
        
        draw.text((cert_x, cert_y), cert_text, font=small_font, fill=(80, 80, 80))  # Slightly darker gray
        
        # Convert to bytes
        img_buffer = BytesIO()
        certificate_img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        # Create HTTP response - display in browser instead of download
        response = HttpResponse(img_buffer.getvalue(), content_type='image/png')
        response['Content-Disposition'] = f'inline; filename="donation_certificate_{certificate.certificate_number}.png"'
        
        return response
        
    except Exception as e:
        print(f"Certificate generation error: {e}")
        # Fallback to PDF generation if image processing fails
        return generate_pdf_certificate(food_listing, certificate)

def generate_pdf_certificate(food_listing, certificate):
    """Fallback PDF certificate generation"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#439249'),
        alignment=TA_CENTER,
        spaceAfter=30,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#166534'),
        alignment=TA_CENTER,
        spaceAfter=20,
        fontName='Helvetica'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.black,
        alignment=TA_CENTER,
        spaceAfter=15,
        fontName='Helvetica'
    )
    
    # Add certificate content
    story.append(Paragraph("CERTIFICATE OF DONATION", title_style))
    story.append(Spacer(1, 20))
    
    # Add decorative line
    story.append(Paragraph("=" * 50, body_style))
    story.append(Spacer(1, 30))
    
    # Certificate text
    certificate_text = f"""
    This is to certify that
    
    <b>{food_listing.donor.user.get_full_name() or food_listing.donor.user.username}</b>
    
    has generously donated food to help reduce waste and feed those in need through the Ek Thaal platform.
    """
    
    story.append(Paragraph(certificate_text, body_style))
    story.append(Spacer(1, 30))
    
    # Donation details
    details_text = f"""
    <b>Donation Details:</b><br/>
    • Food Item: {food_listing.title}<br/>
    • Quantity: {food_listing.quantity} kg<br/>
    • Location: {food_listing.location}<br/>
    • Date: {food_listing.created_at.strftime('%B %d, %Y')}<br/>
    • Certificate Number: {certificate.certificate_number}
    """
    
    story.append(Paragraph(details_text, body_style))
    story.append(Spacer(1, 30))
    
    # Impact statement
    impact_text = """
    <b>Your Impact:</b><br/>
    By donating surplus food, you have helped reduce food waste and provided nourishment to those in need. 
    Your generosity contributes to building a more sustainable and caring community.
    """
    
    story.append(Paragraph(impact_text, body_style))
    story.append(Spacer(1, 40))
    
    # Thank you message
    thank_you_text = """
    <b>Thank you for your kindness and commitment to making a difference!</b>
    """
    
    story.append(Paragraph(thank_you_text, subtitle_style))
    story.append(Spacer(1, 30))
    
    # Footer
    footer_text = f"""
    Issued on: {certificate.issued_at.strftime('%B %d, %Y')}<br/>
    Ek Thaal - Connecting surplus meals to empty plates across Nepal
    """
    
    story.append(Paragraph(footer_text, body_style))
    
    # Build PDF
    doc.build(story)
    
    # Get PDF content
    pdf_content = buffer.getvalue()
    buffer.close()
    
    # Create HTTP response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="donation_certificate_{certificate.certificate_number}.pdf"'
    response.write(pdf_content)
    
    return response
