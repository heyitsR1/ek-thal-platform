#!/usr/bin/env python
"""
Force migration script for Render deployment
"""
import os
import sys
import django
from django.core.management import execute_from_command_line
from django.db import connection, transaction

def force_migrate():
    """Force all migrations to run"""
    print("🚀 Force migrating database...")
    
    try:
        # Set up Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ekthal.settings')
        django.setup()
        
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Database connection successful")
        
        # Force run all migrations
        print("📦 Running all migrations...")
        
        # Run Django system migrations first
        print("  - Running auth migrations...")
        execute_from_command_line(['manage.py', 'migrate', 'auth', '--noinput'])
        
        print("  - Running contenttypes migrations...")
        execute_from_command_line(['manage.py', 'migrate', 'contenttypes', '--noinput'])
        
        print("  - Running sessions migrations...")
        execute_from_command_line(['manage.py', 'migrate', 'sessions', '--noinput'])
        
        print("  - Running admin migrations...")
        execute_from_command_line(['manage.py', 'migrate', 'admin', '--noinput'])
        
        print("  - Running app migrations...")
        execute_from_command_line(['manage.py', 'migrate', 'app', '--noinput'])
        
        # Run general migrate to catch any remaining
        print("  - Running general migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        
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
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = force_migrate()
    sys.exit(0 if success else 1) 