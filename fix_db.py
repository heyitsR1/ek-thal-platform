#!/usr/bin/env python
"""
Manual database fix script for Render
Run this from the Render console if migrations fail
"""
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ekthal.settings')
django.setup()

from django.core.management import call_command
from django.db import connection

def fix_database():
    print("🔧 Fixing database...")
    
    try:
        # Test connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Database connection successful")
        
        # Run all migrations
        print("📦 Running migrations...")
        call_command('migrate', '--noinput')
        
        # Verify tables
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
        print(f"❌ Database fix failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = fix_database()
    sys.exit(0 if success else 1) 