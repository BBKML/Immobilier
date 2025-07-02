#!/usr/bin/env bash

echo "=== EMERGENCY STARTUP SCRIPT ==="

# Vérifier si on est en production
if [ "$DJANGO_DEBUG" = "False" ]; then
    echo "Production environment detected"
    
    echo "Current directory: $(pwd)"
    echo "Python version: $(python --version)"
    
    echo "Checking database..."
    python manage.py check --database default
    
    echo "Removing existing database if it exists..."
    if [ -f "db.sqlite3" ]; then
        rm db.sqlite3
        echo "✅ Database removed"
    else
        echo "ℹ️  No existing database found"
    fi
    
    echo "Creating fresh database..."
    python manage.py migrate --run-syncdb --no-input
    
    echo "Applying all migrations..."
    python manage.py migrate --no-input
    
    echo "Verifying migrations..."
    python manage.py showmigrations
    
    echo "Testing database tables..."
    python manage.py shell << END
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vehicules_vehicule';")
        result = cursor.fetchone()
        if result:
            print("✅ Table vehicules_vehicule exists")
        else:
            print("❌ Table vehicules_vehicule missing - forcing recreation...")
            import os
            if os.path.exists('db.sqlite3'):
                os.remove('db.sqlite3')
            os.system('python manage.py migrate --run-syncdb')
            os.system('python manage.py migrate')
            print("✅ Database recreated and migrations applied")
except Exception as e:
    print(f"❌ Database check failed: {e}")
END
    
    echo "Creating superuser if not exists..."
    python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "admin123")
    print("✅ Superuser 'admin' created")
else:
    print("ℹ️  Superuser 'admin' already exists")
END
    
    echo "Final verification..."
    python manage.py shell << END
from vehicules.models import Vehicule, Moto, Client
try:
    vehicule_count = Vehicule.objects.count()
    moto_count = Moto.objects.count()
    client_count = Client.objects.count()
    print(f"✅ Vehicule count: {vehicule_count}")
    print(f"✅ Moto count: {moto_count}")
    print(f"✅ Client count: {client_count}")
    print("✅ All models accessible!")
except Exception as e:
    print(f"❌ Model test failed: {e}")
END
fi

echo "Starting Gunicorn..."
exec gunicorn gestion_vehicules.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120 