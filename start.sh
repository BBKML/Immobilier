#!/usr/bin/env bash

echo "=== ULTRA AGGRESSIVE STARTUP SCRIPT ==="

# Vérifier si on est en production
if [ "$DJANGO_DEBUG" = "False" ]; then
    echo "Production environment detected"
    
    echo "Current directory: $(pwd)"
    echo "Python version: $(python --version)"
    
    echo "STEP 1: Force remove any existing database..."
    if [ -f "db.sqlite3" ]; then
        rm -f db.sqlite3
        echo "✅ Database removed"
    else
        echo "ℹ️  No existing database found"
    fi
    
    echo "STEP 2: Create fresh database with syncdb..."
    python manage.py migrate --run-syncdb --no-input --verbosity=2
    
    echo "STEP 3: Apply all migrations..."
    python manage.py migrate --no-input --verbosity=2
    
    echo "STEP 4: Verify database creation..."
    python manage.py shell << END
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables in database:")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Check for critical tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auth_user';")
        auth_user_exists = cursor.fetchone()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vehicules_vehicule';")
        vehicule_exists = cursor.fetchone()
        
        if auth_user_exists:
            print("✅ auth_user table exists")
        else:
            print("❌ auth_user table missing")
            
        if vehicule_exists:
            print("✅ vehicules_vehicule table exists")
        else:
            print("❌ vehicules_vehicule table missing")
            
except Exception as e:
    print(f"❌ Database verification failed: {e}")
END
    
    echo "STEP 5: Create superuser..."
    python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "admin123")
    print("✅ Superuser 'admin' created")
else:
    print("ℹ️  Superuser 'admin' already exists")
END
    
    echo "STEP 6: Final test..."
    python manage.py shell << END
from django.contrib.auth import get_user_model
from vehicules.models import Vehicule, Moto, Client
try:
    User = get_user_model()
    user_count = User.objects.count()
    vehicule_count = Vehicule.objects.count()
    moto_count = Moto.objects.count()
    client_count = Client.objects.count()
    print(f"✅ User count: {user_count}")
    print(f"✅ Vehicule count: {vehicule_count}")
    print(f"✅ Moto count: {moto_count}")
    print(f"✅ Client count: {client_count}")
    print("✅ All models accessible!")
except Exception as e:
    print(f"❌ Final test failed: {e}")
END
fi

echo "Starting Gunicorn..."
exec gunicorn gestion_vehicules.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120 