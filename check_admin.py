#!/usr/bin/env python
"""
Check current admin status
"""
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ekthal.settings')
django.setup()

from django.contrib.auth.models import User

def check_admin():
    print("🔍 Checking admin status...")
    
    try:
        # List all users
        users = User.objects.all()
        print(f"📊 Total users: {users.count()}")
        
        for user in users:
            print(f"   - {user.username} ({user.email}) - Staff: {user.is_staff}, Superuser: {user.is_superuser}")
        
        # Check specifically for admin user
        admin_users = User.objects.filter(username='admin')
        if admin_users.exists():
            admin = admin_users.first()
            print(f"\n✅ Admin user found:")
            print(f"   Username: {admin.username}")
            print(f"   Email: {admin.email}")
            print(f"   Is staff: {admin.is_staff}")
            print(f"   Is superuser: {admin.is_superuser}")
            print(f"   Is active: {admin.is_active}")
        else:
            print("\n❌ No admin user found")
            
        return True
        
    except Exception as e:
        print(f"❌ Check failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = check_admin()
    sys.exit(0 if success else 1) 