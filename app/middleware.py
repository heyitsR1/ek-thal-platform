from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db import connection
import os

class DatabaseErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if we're in production and database is not ready
        if os.environ.get('RENDER'):
            try:
                # Test database connection
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
            except Exception as e:
                # If database is not ready, show maintenance page
                if 'relation "django_session" does not exist' in str(e) or 'relation "app_foodlisting" does not exist' in str(e):
                    maintenance_html = render_to_string('maintenance.html')
                    return HttpResponse(maintenance_html, status=503)
        
        response = self.get_response(request)
        return response 