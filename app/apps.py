from django.apps import AppConfig
from django.db import connection
import os


class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"

    def ready(self):
        # Only run migrations in production (Render)
        if os.environ.get('RENDER'):
            try:
                # Test database connection
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                
                # Check if migrations are needed
                from django.core.management import call_command
                from django.db.migrations.executor import MigrationExecutor
                from django.db import connection
                
                executor = MigrationExecutor(connection)
                plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
                
                if plan:
                    print("🔄 Running migrations on startup...")
                    call_command('migrate', '--noinput')
                    print("✅ Migrations completed")
                else:
                    print("✅ Database is up to date")
                
                # Create admin user if it doesn't exist
                from django.contrib.auth.models import User
                if not User.objects.filter(username='admin').exists():
                    print("👤 Creating admin user...")
                    User.objects.create_superuser(
                        username='admin',
                        email='admin@ekthal.com',
                        password='1123'
                    )
                    print("✅ Admin user created")
                else:
                    print("✅ Admin user already exists")
                    
            except Exception as e:
                print(f"⚠️ Migration check failed: {e}")
                # Try to run migrations anyway
                try:
                    from django.core.management import call_command
                    call_command('migrate', '--noinput')
                    print("✅ Migrations completed after retry")
                except Exception as e2:
                    print(f"❌ Migration retry failed: {e2}")
