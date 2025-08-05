from django.core.management.base import BaseCommand
from django.db import connection
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from app.models import Profile, FoodListing

class Command(BaseCommand):
    help = 'Check database connectivity and essential tables'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Checking database connectivity...")
        
        try:
            # Test basic connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                self.stdout.write(self.style.SUCCESS("✅ Database connection successful"))
            
            # Check if django_session table exists
            try:
                Session.objects.count()
                self.stdout.write(self.style.SUCCESS("✅ django_session table exists"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ django_session table missing: {e}"))
            
            # Check if auth_user table exists
            try:
                User.objects.count()
                self.stdout.write(self.style.SUCCESS("✅ auth_user table exists"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ auth_user table missing: {e}"))
            
            # Check if app_profile table exists
            try:
                Profile.objects.count()
                self.stdout.write(self.style.SUCCESS("✅ app_profile table exists"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ app_profile table missing: {e}"))
            
            # Check if app_foodlisting table exists
            try:
                FoodListing.objects.count()
                self.stdout.write(self.style.SUCCESS("✅ app_foodlisting table exists"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ app_foodlisting table missing: {e}"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Database connection failed: {e}")) 