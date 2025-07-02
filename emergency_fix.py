#!/usr/bin/env python
"""
Script d'urgence pour forcer les migrations sur Render
Exécutez ce script dans le shell Render pour résoudre le problème de base de données
"""

import os
import sys
import django
from pathlib import Path

def main():
    print("=== EMERGENCY DATABASE FIX ===")
    
    # Configuration Django
    BASE_DIR = Path(__file__).resolve().parent
    sys.path.append(str(BASE_DIR))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_vehicules.settings')
    
    # Initialiser Django
    django.setup()
    
    from django.core.management import execute_from_command_line
    from django.db import connection
    from django.contrib.auth import get_user_model
    
    try:
        print("1. Checking current directory...")
        print(f"Current directory: {os.getcwd()}")
        print(f"Base directory: {BASE_DIR}")
        
        print("\n2. Checking Django configuration...")
        execute_from_command_line(['manage.py', 'check'])
        
        print("\n3. Checking database status...")
        db_file = BASE_DIR / 'db.sqlite3'
        if db_file.exists():
            print(f"Database file exists: {db_file}")
            print(f"Database size: {db_file.stat().st_size} bytes")
        else:
            print("No database file found")
        
        print("\n4. Removing existing database...")
        if db_file.exists():
            db_file.unlink()
            print("✅ Database removed")
        
        print("\n5. Creating new database...")
        execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
        print("✅ Database created")
        
        print("\n6. Applying all migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ All migrations applied")
        
        print("\n7. Verifying tables...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print("Tables in database:")
            for table in tables:
                print(f"  - {table[0]}")
        
        print("\n8. Testing models...")
        from vehicules.models import Vehicule, Moto, Client
        vehicule_count = Vehicule.objects.count()
        moto_count = Moto.objects.count()
        client_count = Client.objects.count()
        print(f"✅ Vehicule count: {vehicule_count}")
        print(f"✅ Moto count: {moto_count}")
        print(f"✅ Client count: {client_count}")
        
        print("\n9. Creating superuser...")
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin123")
            print("✅ Superuser 'admin' created")
        else:
            print("ℹ️  Superuser 'admin' already exists")
        
        print("\n10. Final verification...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vehicules_vehicule';")
            result = cursor.fetchone()
            if result:
                print("✅ Table vehicules_vehicule exists and is accessible")
            else:
                print("❌ Table vehicules_vehicule still missing!")
                return False
        
        print("\n=== EMERGENCY FIX COMPLETED SUCCESSFULLY ===")
        print("Your application should now work correctly!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    if not success:
        sys.exit(1) 