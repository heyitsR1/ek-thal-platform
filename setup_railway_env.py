#!/usr/bin/env python3
"""
Script to help set up environment variables for Railway deployment
"""
import os
from django.core.management.utils import get_random_secret_key

def main():
    print("🚂 Railway + Neon Deployment Environment Variables")
    print("=" * 50)
    
    # Generate secret key
    secret_key = get_random_secret_key()
    
    print("\n📋 Required Environment Variables for Railway:")
    print("-" * 40)
    
    print(f"SECRET_KEY={secret_key}")
    print("DEBUG=False")
    print("ALLOWED_HOSTS=.railway.app")
    print("CSRF_TRUSTED_ORIGINS=https://*.railway.app")
    print("SITE_URL=https://your-app-name.railway.app")
    print("DATABASE_URL=your_neon_connection_string")
    
    print("\n📧 Optional Email Variables:")
    print("-" * 30)
    print("EMAIL_HOST_USER=your_email@gmail.com")
    print("EMAIL_HOST_PASSWORD=your_app_password")
    
    print("\n☁️ Optional Cloudinary Variables:")
    print("-" * 30)
    print("CLOUDINARY_CLOUD_NAME=your_cloudinary_name")
    print("CLOUDINARY_API_KEY=your_cloudinary_key")
    print("CLOUDINARY_API_SECRET=your_cloudinary_secret")
    
    print("\n🔗 Steps to set up:")
    print("1. Go to Railway dashboard → Variables tab")
    print("2. Add each variable above")
    print("3. Replace placeholder values with your actual values")
    print("4. Get your Neon connection string from neon.tech")
    print("5. Update SITE_URL with your actual Railway app URL")
    
    print("\n💡 Tips:")
    print("- Keep your SECRET_KEY secure and don't share it")
    print("- Use the same SECRET_KEY across deployments")
    print("- Test locally with these variables before deploying")

if __name__ == "__main__":
    main() 