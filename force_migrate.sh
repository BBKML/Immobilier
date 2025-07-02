#!/usr/bin/env bash
# Script de migration forcée pour résoudre les problèmes de base de données

echo "=== Force Migration Script ==="

echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"

echo "Checking Django configuration..."
python manage.py check

echo "Showing current migration status..."
python manage.py showmigrations --verbosity=2

echo "Removing existing database if it exists..."
if [ -f "db.sqlite3" ]; then
    rm db.sqlite3
    echo "🗑️  Removed existing database"
fi

echo "Creating fresh database..."
python manage.py migrate --run-syncdb --verbosity=2

echo "Applying all migrations..."
python manage.py migrate --verbosity=2

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

echo "Creating superuser..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "admin123")
    print("Superuser 'admin' created successfully")
else:
    print("Superuser 'admin' already exists")
END

echo "=== Force migration completed! ===" 