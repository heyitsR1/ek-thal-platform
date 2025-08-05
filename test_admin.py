#!/usr/bin/env python
"""
Test admin creation locally
"""
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ekthal.settings')
django.setup()

from django.contrib.auth.models import User
from django.core.management import call_command

def test_admin():
    print("🧪 Testing admin creation...")
    
    try:
        # First, run migrations
        print("📦 Running migrations...")
        call_command('migrate', '--noinput')
        
        # Check if admin user exists
        if User.objects.filter(username='admin').exists():
            print("✅ Admin user exists")
            admin_user = User.objects.get(username='admin')
            print(f"   Username: {admin_user.username}")
            print(f"   Email: {admin_user.email}")
            print(f"   Is staff: {admin_user.is_staff}")
            print(f"   Is superuser: {admin_user.is_superuser}")
            
            # Update password
            admin_user.set_password('1123')
            admin_user.save()
            print("✅ Password updated to '1123'")
        else:
            print("❌ Admin user does not exist, creating...")
            User.objects.create_superuser(
                username='admin',
                email='aarohan.niraula@westcliff.edu',
                password='1123'
            )
            print("✅ Admin user created")
        
        # Test login
        print("🔐 Testing login...")
        from django.contrib.auth import authenticate
        user = authenticate(username='admin', password='1123')
        if user:
            print("✅ Login successful!")
            print(f"   User: {user.username}")
            print(f"   Email: {user.email}")
            print(f"   Is staff: {user.is_staff}")
            print(f"   Is superuser: {user.is_superuser}")
        else:
            print("❌ Login failed!")
            
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_admin()
    sys.exit(0 if success else 1) 