#!/usr/bin/env bash

echo "Starting EkThal application..."

# Wait a moment for database to be ready
sleep 2

# Check if database is ready
echo "Checking database readiness..."
python manage.py check_db

# If database check fails, try to initialize it
if [ $? -ne 0 ]; then
    echo "Database not ready, attempting initialization..."
    python init_db.py
fi

# Start the application
echo "Starting Gunicorn server..."
gunicorn ekthal.wsgi:application --bind 0.0.0.0:$PORT 