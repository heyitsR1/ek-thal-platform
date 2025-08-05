from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create admin user with username: admin, password: 1123'

    def handle(self, *args, **options):
        try:
            # Check if admin user already exists
            if User.objects.filter(username='admin').exists():
                self.stdout.write("✅ Admin user already exists")
                # Update password
                admin_user = User.objects.get(username='admin')
                admin_user.set_password('1123')
                admin_user.is_staff = True
                admin_user.is_superuser = True
                admin_user.save()
                self.stdout.write(self.style.SUCCESS("✅ Admin password updated"))
            else:
                # Create new admin user
                User.objects.create_superuser(
                    username='admin',
                    email='admin@ekthal.com',
                    password='1123'
                )
                self.stdout.write(self.style.SUCCESS("✅ Admin user created successfully"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Failed to create admin user: {e}")) 