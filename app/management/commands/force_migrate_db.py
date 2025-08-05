from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection

class Command(BaseCommand):
    help = 'Force run all database migrations'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Force running all migrations...")
        
        try:
            # Test database connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                self.stdout.write(self.style.SUCCESS("✅ Database connection successful"))
            
            # Run all migrations
            self.stdout.write("📦 Running Django system migrations...")
            call_command('migrate', 'auth', '--noinput')
            call_command('migrate', 'contenttypes', '--noinput')
            call_command('migrate', 'sessions', '--noinput')
            call_command('migrate', 'admin', '--noinput')
            call_command('migrate', 'app', '--noinput')
            call_command('migrate', '--noinput')
            
            # Verify tables
            self.stdout.write("🔍 Verifying tables...")
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
                    self.stdout.write(self.style.ERROR(f"❌ Missing tables: {missing_tables}"))
                else:
                    self.stdout.write(self.style.SUCCESS("✅ All required tables exist"))
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Migration failed: {e}"))
            import traceback
            traceback.print_exc() 