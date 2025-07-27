#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Checking database connection..."
python manage.py check --database default

echo "Running migrations..."
python manage.py migrate --noinput

echo "Checking database tables..."
python manage.py check_db

echo "Showing migration status..."
python manage.py showmigrations

echo "Build completed successfully!" 