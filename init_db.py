#!/usr/bin/env python
"""
Database initialization script for Render deployment
"""
import os
import sys
import django
from django.core.management import execute_from_command_line
from django.db import connection

def init_database():
    """Initialize the database with all required tables"""
    print("🔧 Initializing database...")
    
    try:
        # Set up Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ekthal.settings')
        django.setup()
        
        # Check if we can connect to the database
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Database connection successful")
        
        # Run all migrations
        print("📦 Running Django system migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        
        # Run app-specific migrations
        print("📦 Running app migrations...")
        execute_from_command_line(['manage.py', 'migrate', 'app', '--noinput'])
        
        # Verify tables exist
        print("🔍 Verifying tables...")
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN ('django_session', 'auth_user', 'app_profile', 'app_foodlisting')
                ORDER BY table_name
            """)
            tables = [row[0] for row in cursor.fetchall()]
            
            required_tables = ['django_session', 'auth_user', 'app_profile', 'app_foodlisting']
            missing_tables = [table for table in required_tables if table not in tables]
            
            if missing_tables:
                print(f"❌ Missing tables: {missing_tables}")
                return False
            else:
                print("✅ All required tables exist")
                return True
                
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 1) 