#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "Verifying static files..."
ls -la staticfiles/images/ || echo "Warning: images directory not found in staticfiles"
ls -la staticfiles/ || echo "Warning: staticfiles directory is empty"

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Build completed successfully!" 