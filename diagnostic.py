#!/usr/bin/env python
"""
Script de diagnostic pour identifier les problèmes de base de données
"""
import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_vehicules.settings')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line
from django.conf import settings

def check_database():
    """Vérifier l'état de la base de données"""
    print("=== DIAGNOSTIC DE LA BASE DE DONNÉES ===")
    
    # 1. Vérifier la configuration de la base de données
    print(f"\n1. Configuration de la base de données:")
    print(f"   - ENGINE: {settings.DATABASES['default']['ENGINE']}")
    print(f"   - NAME: {settings.DATABASES['default']['NAME']}")
    print(f"   - DEBUG: {settings.DEBUG}")
    
    # 2. Vérifier la connexion
    print(f"\n2. Test de connexion à la base de données:")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT sqlite_version();")
            version = cursor.fetchone()
            print(f"   ✅ Connexion réussie - SQLite version: {version[0]}")
    except Exception as e:
        print(f"   ❌ Erreur de connexion: {e}")
        return False
    
    # 3. Lister les tables existantes
    print(f"\n3. Tables existantes dans la base de données:")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            if tables:
                for table in tables:
                    print(f"   - {table[0]}")
            else:
                print("   ⚠️  Aucune table trouvée!")
    except Exception as e:
        print(f"   ❌ Erreur lors de la lecture des tables: {e}")
        return False
    
    # 4. Vérifier les migrations
    print(f"\n4. Statut des migrations:")
    try:
        from django.core.management import call_command
        from io import StringIO
        
        # Capturer la sortie de showmigrations
        out = StringIO()
        call_command('showmigrations', stdout=out)
        migrations_output = out.getvalue()
        
        # Analyser la sortie
        lines = migrations_output.split('\n')
        for line in lines:
            if 'vehicules' in line:
                print(f"   {line}")
    except Exception as e:
        print(f"   ❌ Erreur lors de la vérification des migrations: {e}")
    
    # 5. Vérifier les modèles
    print(f"\n5. Test des modèles Django:")
    try:
        from vehicules.models import Vehicule, Moto, Client, Proprietaire, Marque
        
        # Test de création d'objets (sans sauvegarder)
        print("   ✅ Import des modèles réussi")
        
        # Compter les objets existants
        try:
            vehicule_count = Vehicule.objects.count()
            moto_count = Moto.objects.count()
            client_count = Client.objects.count()
            proprietaire_count = Proprietaire.objects.count()
            marque_count = Marque.objects.count()
            
            print(f"   - Véhicules: {vehicule_count}")
            print(f"   - Motos: {moto_count}")
            print(f"   - Clients: {client_count}")
            print(f"   - Propriétaires: {proprietaire_count}")
            print(f"   - Marques: {marque_count}")
            
        except Exception as e:
            print(f"   ❌ Erreur lors du comptage: {e}")
            
    except Exception as e:
        print(f"   ❌ Erreur lors de l'import des modèles: {e}")
    
    return True

def apply_migrations():
    """Appliquer les migrations"""
    print(f"\n=== APPLICATION DES MIGRATIONS ===")
    
    try:
        from django.core.management import call_command
        
        print("1. Application des migrations...")
        call_command('migrate', verbosity=2)
        
        print("2. Vérification finale...")
        call_command('showmigrations', verbosity=2)
        
        print("✅ Migrations appliquées avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'application des migrations: {e}")
        return False

def create_superuser():
    """Créer un superuser par défaut"""
    print(f"\n=== CRÉATION DU SUPERUSER ===")
    
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin123")
            print("✅ Superuser 'admin' créé avec succès!")
        else:
            print("ℹ️  Superuser 'admin' existe déjà")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du superuser: {e}")
        return False

if __name__ == "__main__":
    print("Démarrage du diagnostic...")
    
    # Exécuter les diagnostics
    db_ok = check_database()
    
    if db_ok:
        # Appliquer les migrations si nécessaire
        if apply_migrations():
            create_superuser()
    
    print(f"\n=== DIAGNOSTIC TERMINÉ ===") 