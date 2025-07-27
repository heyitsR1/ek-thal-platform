#!/usr/bin/env bash

echo "Starting EkThal application..."

# Wait a moment for database to be ready
sleep 2

# Check if database is ready
echo "Checking database readiness..."
python manage.py check_db

# Start the application
echo "Starting Gunicorn server..."
gunicorn ekthal.wsgi:application --bind 0.0.0.0:$PORT 