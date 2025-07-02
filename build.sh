#!/usr/bin/env bash
# exit on error
set -o errexit

echo "=== Starting build process ==="

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "Checking database connection..."
python manage.py check --database default

echo "Showing migration status..."
python manage.py showmigrations

echo "Applying migrations..."
python manage.py migrate --no-input --verbosity=2

echo "Verifying migrations..."
python manage.py showmigrations --verbosity=2

echo "Creating default superuser (if not exists)..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "admin123")
    print("Superuser 'admin' created successfully")
else:
    print("Superuser 'admin' already exists")
END

echo "=== Build completed successfully! ==="
