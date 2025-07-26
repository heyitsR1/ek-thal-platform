#!/usr/bin/env python
"""
Test script for WhatsApp API integration
Run this to test your WhatsApp configuration
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ekthal.settings')
django.setup()

from app.whatsapp import whatsapp
from app.models import FoodListing, Profile
from django.contrib.auth.models import User

def test_whatsapp_config():
    """Test WhatsApp configuration"""
    print("🔧 Testing WhatsApp Configuration...")
    print(f"API URL: {whatsapp.api_url}")
    print(f"API Key: {'✅ Set' if whatsapp.api_key else '❌ Not set'}")
    print(f"Phone Number ID: {'✅ Set' if whatsapp.phone_number_id else '❌ Not set'}")
    print(f"Admin Phone: {'✅ Set' if whatsapp.admin_phone else '❌ Not set'}")
    
    if not all([whatsapp.api_url, whatsapp.api_key, whatsapp.phone_number_id]):
        print("\n❌ WhatsApp API not fully configured!")
        print("Please set the following in settings.py:")
        print("- WHATSAPP_API_KEY")
        print("- WHATSAPP_PHONE_NUMBER_ID")
        print("- ADMIN_WHATSAPP_NUMBER")
        return False
    
    return True

def test_admin_notification():
    """Test admin notification"""
    print("\n📱 Testing Admin Notification...")
    
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
            description="Test food listing for WhatsApp notification",
            status='pending'
        )
        
        # Send test notification
        success = whatsapp.notify_admin_new_listing(listing)
        
        if success:
            print("✅ Admin notification sent successfully!")
        else:
            print("❌ Admin notification failed!")
            
        # Clean up test listing
        listing.delete()
        return success
        
    except Exception as e:
        print(f"❌ Error testing admin notification: {e}")
        return False

def test_receiver_notification():
    """Test receiver notification"""
    print("\n📱 Testing Receiver Notification...")
    
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
        receivers_notified = whatsapp.notify_receivers_new_listing(listing)
        
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

if __name__ == "__main__":
    print("🚀 WhatsApp API Test Suite")
    print("=" * 40)
    
    # Test configuration
    if not test_whatsapp_config():
        exit(1)
    
    # Test notifications
    test_admin_notification()
    test_receiver_notification()
    
    print("\n✅ Test completed!")
    print("\n📝 Next steps:")
    print("1. Configure your WhatsApp API credentials in settings.py")
    print("2. Run this test again to verify everything works")
    print("3. Start using the app - notifications will be sent automatically!") 