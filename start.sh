#!/usr/bin/env bash

echo "Starting EkThal application..."

# Wait a moment for database to be ready
sleep 5

# Always run migrations on startup
echo "Running migrations on startup..."
python force_migrate.py

# Check database status
echo "Checking database status..."
python manage.py check_db

# Start the application
echo "Starting Gunicorn server..."
gunicorn ekthal.wsgi:application --bind 0.0.0.0:$PORT 