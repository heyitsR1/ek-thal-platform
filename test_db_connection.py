#!/usr/bin/env python3
"""
Test script to verify Neon database connection
"""
import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ekthal.settings')
django.setup()

def test_database_connection():
    """Test the database connection"""
    try:
        from django.db import connection
        from django.core.management import execute_from_command_line
        
        print("🔍 Testing database connection...")
        
        # Test basic connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"✅ Database connection successful: {result}")
        
        # Test Django check
        print("🔍 Running Django system check...")
        execute_from_command_line(['manage.py', 'check'])
        print("✅ Django system check passed")
        
        # Test migrations
        print("🔍 Testing migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--check'])
        print("✅ Migrations check passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    # Set the DATABASE_URL for testing
    database_url = "postgresql://neondb_owner:npg_DQF3McXgqPt8@ep-red-morning-adxqaxae-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    os.environ['DATABASE_URL'] = database_url
    os.environ['DEBUG'] = 'False'
    
    success = test_database_connection()
    if success:
        print("🎉 All tests passed! Database is ready for deployment.")
    else:
        print("💥 Tests failed. Please check your database configuration.") 