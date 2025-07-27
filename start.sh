#!/usr/bin/env bash

echo "Starting EkThal application..."

# Wait a moment for database to be ready
sleep 2

# Check if database is ready
echo "Checking database readiness..."
python manage.py check_db

# If database check fails, try to force migrate
if [ $? -ne 0 ]; then
    echo "Database not ready, attempting force migration..."
    python force_migrate.py
    
    # Check again after migration
    echo "Checking database after migration..."
    python manage.py check_db
fi

# Start the application
echo "Starting Gunicorn server..."
gunicorn ekthal.wsgi:application --bind 0.0.0.0:$PORT 