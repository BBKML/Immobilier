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

echo "Checking if database exists and has tables..."
python manage.py shell << END
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vehicules_vehicule';")
        table_exists = cursor.fetchone()
        if table_exists:
            print("✅ Table vehicules_vehicule exists")
        else:
            print("❌ Table vehicules_vehicule does not exist - forcing migration")
            import os
            if os.path.exists('db.sqlite3'):
                os.remove('db.sqlite3')
                print("🗑️  Removed existing database")
END

echo "Applying migrations..."
python manage.py migrate --no-input --verbosity=2

echo "Verifying migrations..."
python manage.py showmigrations --verbosity=2

echo "Testing database tables..."
python manage.py shell << END
from django.db import connection
from vehicules.models import Vehicule, Moto, Client, Proprietaire, Marque

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables in database:")
        for table in tables:
            print(f"  - {table[0]}")
    
    # Test model access
    vehicule_count = Vehicule.objects.count()
    print(f"✅ Vehicule model accessible - count: {vehicule_count}")
    
except Exception as e:
    print(f"❌ Database test failed: {e}")
    exit(1)
END

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
