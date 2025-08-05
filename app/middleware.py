from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db import connection
<<<<<<< HEAD
=======
from django.middleware.csrf import get_token
>>>>>>> b4c8a48ade4829f0e06836e4cb3da3911c17ed0a
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
<<<<<<< HEAD
=======
        return response

class CSRFDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Ensure CSRF token is set for all requests
        if request.method == 'GET':
            get_token(request)
        
        response = self.get_response(request)
>>>>>>> b4c8a48ade4829f0e06836e4cb3da3911c17ed0a
        return response 