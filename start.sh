#!/usr/bin/env bash

echo "=== Starting application with forced migrations ==="

# Vérifier si on est en production
if [ "$DJANGO_DEBUG" = "False" ]; then
    echo "Production environment detected"
    
    echo "Checking database..."
    python manage.py check --database default
    
    echo "Showing migration status..."
    python manage.py showmigrations
    
    echo "Forcing migrations..."
    python manage.py migrate --no-input --run-syncdb
    
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
            print("❌ Table vehicules_vehicule missing - creating database...")
            import os
            if os.path.exists('db.sqlite3'):
                os.remove('db.sqlite3')
            os.system('python manage.py migrate --run-syncdb')
            print("✅ Database created and migrations applied")
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
fi

echo "Starting Gunicorn..."
exec gunicorn gestion_vehicules.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120 