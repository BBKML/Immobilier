#!/usr/bin/env python
"""
Script d'urgence pour forcer les migrations Django
À exécuter manuellement si les migrations ne s'appliquent pas automatiquement
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
    print("=== EMERGENCY MIGRATION SCRIPT ===")
    
    try:
        # Vérifier la configuration
        print("1. Checking Django configuration...")
        execute_from_command_line(['manage.py', 'check'])
        
        # Supprimer la base de données si elle existe
        db_file = BASE_DIR / 'db.sqlite3'
        if db_file.exists():
            print("2. Removing existing database...")
            db_file.unlink()
            print("✅ Database removed")
        
        # Créer une nouvelle base de données
        print("3. Creating new database...")
        execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
        
        # Appliquer toutes les migrations
        print("4. Applying all migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        # Vérifier les tables
        print("5. Verifying tables...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print("Tables in database:")
            for table in tables:
                print(f"  - {table[0]}")
        
        # Créer le superuser
        print("6. Creating superuser...")
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin123")
            print("✅ Superuser 'admin' created")
        else:
            print("ℹ️  Superuser 'admin' already exists")
        
        print("=== MIGRATION COMPLETED SUCCESSFULLY ===")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main() 