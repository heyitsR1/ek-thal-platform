#!/usr/bin/env python
"""
Create admin user script for Render deployment
"""
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ekthal.settings')
django.setup()

from django.contrib.auth.models import User
from django.core.management import call_command

def create_admin():
    print("👤 Creating admin user...")
    
    try:
        # Check if admin user already exists
        if User.objects.filter(username='admin').exists():
            print("✅ Admin user already exists")
            # Update password
            admin_user = User.objects.get(username='admin')
            admin_user.set_password('1123')
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            print("✅ Admin password updated")
            return True
        else:
            # Create new admin user
            User.objects.create_superuser(
                username='admin',
                email='admin@ekthal.com',
                password='1123'
            )
            print("✅ Admin user created successfully")
            return True
            
    except Exception as e:
        print(f"❌ Failed to create admin user: {e}")
        return False

if __name__ == '__main__':
    success = create_admin()
    sys.exit(0 if success else 1) 