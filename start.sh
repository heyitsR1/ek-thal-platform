#!/usr/bin/env bash

echo "Starting EkThal application..."

# Wait a moment for database to be ready
sleep 5

# Always run migrations on startup
echo "Running migrations on startup..."
python manage.py migrate --noinput

# Check database status
echo "Checking database status..."
python manage.py check_db

# Create admin user if it doesn't exist
echo "Creating admin user..."
python create_admin.py

# Start the application
echo "Starting Gunicorn server..."
gunicorn ekthal.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120 