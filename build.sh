#!/usr/bin/env bash
# exit on error
set -o errexit

echo "=== Starting build process ==="

echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "Checking Django configuration..."
python manage.py check

echo "Showing migration status before applying..."
python manage.py showmigrations --verbosity=2

echo "Checking database connection..."
python manage.py check --database default

echo "Forcing migration application..."
python manage.py migrate --no-input --verbosity=2 --run-syncdb

echo "Showing migration status after applying..."
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
    
    # Test other models
    moto_count = Moto.objects.count()
    client_count = Client.objects.count()
    print(f"✅ Moto model accessible - count: {moto_count}")
    print(f"✅ Client model accessible - count: {client_count}")
    
except Exception as e:
    print(f"❌ Database test failed: {e}")
    import traceback
    traceback.print_exc()
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

echo "Final database check..."
python manage.py shell << END
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vehicules_vehicule';")
    result = cursor.fetchone()
    if result:
        print("✅ Table vehicules_vehicule exists and is accessible")
    else:
        print("❌ Table vehicules_vehicule still missing!")
        exit(1)
END

echo "=== Build completed successfully! ==="
