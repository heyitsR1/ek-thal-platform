"""
URL configuration for ekthal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("register/", views.register, name="register"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register_individual/", views.register_individual, name="register_individual"),
    path("register_organization/", views.register_organization, name="register_organization"),
    path("food_listing_form/", views.food_listing_form, name="food_listing_form"),
    path("thank_you/", views.thank_you, name="thank_you"),
    path("listings/", views.listings, name="listings"),
    path("listing/<int:listing_id>/", views.listing_detail, name="listing_detail"),
    path("claim/<int:listing_id>/", views.claim_listing, name="claim_listing"),
    path("connection/<int:claimed_listing_id>/", views.connection_page, name="connection_page"),
    path("receiver_dashboard/", views.receiver_dashboard, name="receiver_dashboard"),
    path("dashboard/pending-listings/", views.dashboard_pending_listings, name="dashboard_pending_listings"),
    path("dashboard/approve-listing/<int:listing_id>/", views.dashboard_approve_listing, name="dashboard_approve_listing"),
]

# Serve media files in development only
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
