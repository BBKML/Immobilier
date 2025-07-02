#!/usr/bin/env bash
# exit on error
set -o errexit

echo "=== Starting build process ==="

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "Verifying static files..."
ls -la staticfiles/images/ || echo "Warning: images directory not found in staticfiles"

echo "Checking database status..."
python manage.py showmigrations

echo "Running database migrations..."
python manage.py migrate --no-input

echo "=== Build completed successfully! ===" 