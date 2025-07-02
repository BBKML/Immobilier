#!/usr/bin/env python
"""
Script de migration d'urgence pour Render
Exécutez ce script directement sur Render pour forcer les migrations
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_vehicules.settings')

# Initialiser Django
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection
from django.contrib.auth import get_user_model

def main():
    print("=== URGENCY MIGRATION SCRIPT ===")
    print(f"Current directory: {os.getcwd()}")
    print(f"Base directory: {BASE_DIR}")
    
    try:
        # 1. Vérifier la configuration
        print("\n1. Checking Django configuration...")
        execute_from_command_line(['manage.py', 'check'])
        
        # 2. Supprimer la base de données si elle existe
        db_file = BASE_DIR / 'db.sqlite3'
        if db_file.exists():
            print(f"\n2. Removing existing database: {db_file}")
            db_file.unlink()
            print("✅ Database removed")
        else:
            print(f"\n2. No existing database found at: {db_file}")
        
        # 3. Créer une nouvelle base de données
        print("\n3. Creating new database...")
        execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
        print("✅ Database created")
        
        # 4. Appliquer toutes les migrations
        print("\n4. Applying all migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ All migrations applied")
        
        # 5. Vérifier les tables
        print("\n5. Verifying tables...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print("Tables in database:")
            for table in tables:
                print(f"  - {table[0]}")
        
        # 6. Créer le superuser
        print("\n6. Creating superuser...")
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin123")
            print("✅ Superuser 'admin' created")
        else:
            print("ℹ️  Superuser 'admin' already exists")
        
        # 7. Test final
        print("\n7. Final test...")
        from vehicules.models import Vehicule, Moto, Client
        vehicule_count = Vehicule.objects.count()
        moto_count = Moto.objects.count()
        client_count = Client.objects.count()
        print(f"✅ Vehicule count: {vehicule_count}")
        print(f"✅ Moto count: {moto_count}")
        print(f"✅ Client count: {client_count}")
        
        print("\n=== MIGRATION COMPLETED SUCCESSFULLY ===")
        print("Your application should now work correctly!")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main() 