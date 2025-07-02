"""
WSGI config for gestion_vehicules project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys
import subprocess
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_vehicules.settings')

# Forcer les migrations au démarrage en production
if os.environ.get('DJANGO_DEBUG', 'True').lower() == 'false':
    try:
        # Vérifier si on est dans le bon répertoire
        project_dir = Path(__file__).resolve().parent.parent
        os.chdir(project_dir)
        
        print("=== FORCING MIGRATIONS AT STARTUP ===")
        
        # Vérifier si la base de données existe
        db_file = project_dir / 'db.sqlite3'
        if not db_file.exists():
            print("Database file not found, creating...")
            subprocess.run([sys.executable, 'manage.py', 'migrate', '--run-syncdb'], check=True)
            print("✅ Database created")
        else:
            print("Database file exists, applying migrations...")
            subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
            print("✅ Migrations applied")
        
        # Créer le superuser si nécessaire
        subprocess.run([sys.executable, 'manage.py', 'shell', '-c', 
                       'from django.contrib.auth import get_user_model; '
                       'User = get_user_model(); '
                       'if not User.objects.filter(username="admin").exists(): '
                       'User.objects.create_superuser("admin", "admin@example.com", "admin123"); '
                       'print("Superuser created")'], check=True)
        
        print("=== STARTUP MIGRATIONS COMPLETED ===")
        
    except Exception as e:
        print(f"❌ Error during startup migrations: {e}")
        # Continuer même en cas d'erreur

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
