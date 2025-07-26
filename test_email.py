#!/usr/bin/env python
"""
Test script for email notifications
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ekthal.settings')
django.setup()

from app.email_notifications import email_notifier
from app.models import FoodListing, Profile
from django.contrib.auth.models import User

def test_email_config():
    """Test email configuration"""
    print("🔧 Testing Email Configuration...")
    print(f"From Email: {email_notifier.from_email}")
    print(f"Admin Emails: {email_notifier.admin_emails}")
    
    if not email_notifier.admin_emails:
        print("\n❌ No admin emails configured!")
        print("Please set ADMINS in settings.py:")
        return False
    
    return True

def test_admin_notification():
    """Test admin notification"""
    print("\n📧 Testing Admin Notification...")
    
    # Create a test listing
    try:
        user = User.objects.first()
        if not user:
            print("❌ No users found. Please create a user first.")
            return False
            
        profile = Profile.objects.get(user=user)
        
        # Create a test listing
        listing = FoodListing.objects.create(
            donor=profile,
            title="TEST - Fresh Bread",
            location="Test Location",
            quantity=5.0,
            description="Test food listing for email notification",
            status='pending'
        )
        
        # Send test notification
        success = email_notifier.send_admin_new_listing_notification(listing)
        
        if success:
            print("✅ Admin notification email sent successfully!")
        else:
            print("❌ Admin notification email failed!")
            
        # Clean up test listing
        listing.delete()
        return success
        
    except Exception as e:
        print(f"❌ Error testing admin notification: {e}")
        return False

def test_receiver_notification():
    """Test receiver notification"""
    print("\n📧 Testing Receiver Notification...")
    
    # Create a test listing
    try:
        user = User.objects.first()
        if not user:
            print("❌ No users found. Please create a user first.")
            return False
            
        profile = Profile.objects.get(user=user)
        
        # Create a test listing
        listing = FoodListing.objects.create(
            donor=profile,
            title="TEST - Fresh Vegetables",
            location="Test Location",
            quantity=3.0,
            description="Test food listing for receiver notification",
            status='approved'
        )
        
        # Send test notification
        receivers_notified = email_notifier.send_receivers_new_listing_notification(listing)
        
        if receivers_notified > 0:
            print(f"✅ Notified {receivers_notified} receivers successfully!")
        else:
            print("⚠️ No receivers to notify or notification failed!")
            
        # Clean up test listing
        listing.delete()
        return receivers_notified > 0
        
    except Exception as e:
        print(f"❌ Error testing receiver notification: {e}")
        return False

def test_donor_notification():
    """Test donor notification"""
    print("\n📧 Testing Donor Notification...")
    
    # Create a test listing
    try:
        user = User.objects.first()
        if not user:
            print("❌ No users found. Please create a user first.")
            return False
            
        profile = Profile.objects.get(user=user)
        
        # Create a test listing
        listing = FoodListing.objects.create(
            donor=profile,
            title="TEST - Fresh Fruits",
            location="Test Location",
            quantity=2.0,
            description="Test food listing for donor notification",
            status='approved'
        )
        
        # Send test notification
        success = email_notifier.send_donor_listing_approved_notification(listing)
        
        if success:
            print("✅ Donor notification email sent successfully!")
        else:
            print("❌ Donor notification email failed!")
            
        # Clean up test listing
        listing.delete()
        return success
        
    except Exception as e:
        print(f"❌ Error testing donor notification: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Email Notification Test Suite")
    print("=" * 40)
    
    # Test configuration
    if not test_email_config():
        exit(1)
    
    # Test notifications
    test_admin_notification()
    test_receiver_notification()
    test_donor_notification()
    
    print("\n✅ Test completed!")
    print("\n📝 Next steps:")
    print("1. Configure email credentials in settings.py")
    print("2. For Gmail, use an App Password")
    print("3. Run this test again to verify everything works")
    print("4. Start using the app - emails will be sent automatically!")
    
    print("\n🔧 Email Setup Instructions:")
    print("1. Update EMAIL_HOST_USER with your Gmail address")
    print("2. Update EMAIL_HOST_PASSWORD with your Gmail App Password")
    print("3. Update ADMINS with your admin email address")
    print("4. For testing, use console backend: EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'") 