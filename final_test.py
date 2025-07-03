#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test final pour vérifier que tous les composants fonctionnent
"""

import os
import json
import sys

def test_json_files():
    """Teste tous les fichiers JSON"""
    print("🔍 Test des fichiers JSON...")
    
    json_files = [
        'data_backup.json',
        'local_data_backup.json',
        'vehicules_data.json',
        'clean_data_backup.json'
    ]
    
    valid_files = 0
    for file_path in json_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"✅ {file_path}: {len(data)} objets")
                valid_files += 1
            except Exception as e:
                print(f"❌ {file_path}: {e}")
        else:
            print(f"⚠️ {file_path}: Fichier non trouvé")
    
    return valid_files >= 1  # Au moins un fichier JSON valide

def test_django_commands():
    """Teste les commandes Django"""
    print("\n🔍 Test des commandes Django...")
    
    try:
        import os
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_vehicules.settings')
        
        import django
        django.setup()
        
        from django.core.management import call_command
        from django.core.management.base import CommandError
        
        # Test de la commande de sauvegarde
        print("🔄 Test de la commande backup_local_data...")
        call_command('backup_local_data', verbosity=0)
        print("✅ Commande backup_local_data fonctionne")
        
        # Test de la commande d'import
        print("🔄 Test de la commande import_local_data...")
        call_command('import_local_data', verbosity=0)
        print("✅ Commande import_local_data fonctionne")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test Django: {e}")
        return False

def test_database():
    """Teste la base de données"""
    print("\n🔍 Test de la base de données...")
    
    try:
        import os
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_vehicules.settings')
        
        import django
        django.setup()
        
        from vehicules.models import Vehicule, Client, Marque
        
        # Compter les objets
        vehicules_count = Vehicule.objects.count()
        clients_count = Client.objects.count()
        marques_count = Marque.objects.count()
        
        print(f"✅ Véhicules: {vehicules_count}")
        print(f"✅ Clients: {clients_count}")
        print(f"✅ Marques: {marques_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test de la base de données: {e}")
        return False

def main():
    """Fonction principale"""
    print("🧪 TEST FINAL DU SYSTÈME")
    print("=" * 50)
    
    # Tests
    json_ok = test_json_files()
    django_ok = test_django_commands()
    db_ok = test_database()
    
    print("\n📊 RÉSULTATS DES TESTS")
    print("=" * 30)
    print(f"📄 Fichiers JSON: {'✅' if json_ok else '❌'}")
    print(f"🐍 Commandes Django: {'✅' if django_ok else '❌'}")
    print(f"🗄️ Base de données: {'✅' if db_ok else '❌'}")
    
    if json_ok and django_ok and db_ok:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS!")
        print("✅ Votre système est prêt pour le déploiement sur Render")
        print("\n💡 Prochaines étapes:")
        print("   1. Le déploiement sur Render va automatiquement:")
        print("      - Appliquer les migrations")
        print("      - Créer un superuser")
        print("      - Importer vos données locales")
        print("   2. Vos données seront disponibles sur Render")
        print("   3. L'application sera accessible en production")
    else:
        print("\n⚠️ Certains tests ont échoué")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main() 