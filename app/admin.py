from django.contrib import admin
from .models import Profile, FoodListing, ClaimedListing, Rating, Certificate

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_organization', 'is_receiver', 'phone_number_1']
    list_filter = ['is_organization', 'is_receiver']
    search_fields = ['user__username', 'user__email', 'phone_number_1']

@admin.register(FoodListing)
class FoodListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'donor', 'quantity', 'location', 'status', 'created_at']
    list_filter = ['status', 'recurring', 'created_at']
    search_fields = ['title', 'description', 'donor__user__username']
    readonly_fields = ['created_at']

@admin.register(ClaimedListing)
class ClaimedListingAdmin(admin.ModelAdmin):
    list_display = ['food_listing', 'organization', 'claimed_at']
    list_filter = ['claimed_at']
    search_fields = ['food_listing__title', 'organization__user__username']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['rater', 'ratee', 'score', 'claimed_listing', 'created_at']
    list_filter = ['score', 'created_at']
    search_fields = ['rater__user__username', 'ratee__user__username']

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['certificate_number', 'donor', 'food_listing', 'issued_at']
    list_filter = ['issued_at']
    search_fields = ['certificate_number', 'donor__user__username', 'food_listing__title']
    readonly_fields = ['certificate_number', 'issued_at']


