from django.contrib.auth.models import User
from django.db import models
import uuid
from datetime import datetime


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_organization = models.BooleanField(default=False)
    is_receiver = models.BooleanField(default=False)
    phone_number_1 = models.CharField(max_length=20)
    phone_number_2 = models.CharField(max_length=20, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class FoodListing(models.Model):
    donor = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, help_text='Required')
    description = models.TextField(help_text='Required')
    location = models.CharField(max_length=255, help_text='Required')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    quantity = models.FloatField(help_text='Quantity in kg (Required)')
    prepared_at = models.DateTimeField(null=True, blank=True, help_text='Date and hour food was prepared (Required)')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)
    ai_report = models.TextField(blank=True)
    recurring = models.BooleanField(default=False)
    storage = models.CharField(max_length=50, blank=True, help_text='Required')
    prepared_by = models.CharField(max_length=50, blank=True, help_text='Required')
    special_instructions = models.TextField(blank=True, help_text='Optional')
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')

    def __str__(self):
        return self.title
    
class ClaimedListing(models.Model):
    food_listing = models.ForeignKey(FoodListing, on_delete=models.CASCADE)
    organization = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='claimed_listings')
    claimed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.organization.user.username} claimed {self.food_listing.title}"

class Rating(models.Model):
    rater = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='given_ratings')
    ratee = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_ratings')
    claimed_listing = models.ForeignKey(ClaimedListing, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('rater', 'claimed_listing')  # Prevent double rating per transaction

    def __str__(self):
        return f"{self.rater.user.username} rated {self.ratee.user.username} ({self.score})"

class Certificate(models.Model):
    """Model to track donation certificates issued to donors"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    donor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='certificates')
    food_listing = models.ForeignKey(FoodListing, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_number = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return f"Certificate {self.certificate_number} - {self.donor.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.certificate_number:
            # Generate certificate number: EK-YYYY-XXXX
            year = self.issued_at.year if self.issued_at else datetime.now().year
            last_cert = Certificate.objects.filter(
                certificate_number__startswith=f'EK-{year}-'
            ).order_by('-certificate_number').first()
            
            if last_cert:
                last_num = int(last_cert.certificate_number.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
                
            self.certificate_number = f'EK-{year}-{new_num:04d}'
        
        super().save(*args, **kwargs)
