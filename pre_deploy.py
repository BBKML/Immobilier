#!/usr/bin/env python
"""
Script de pré-déploiement pour sauvegarder automatiquement les données locales
Exécutez ce script avant chaque push vers GitHub
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_vehicules.settings')
django.setup()

from django.core.management import call_command

def main():
    print("🔄 Sauvegarde automatique des données locales...")
    
    try:
        # Créer la sauvegarde
        call_command('backup_local_data')
        
        print("✅ Sauvegarde terminée!")
        print("📤 Vous pouvez maintenant pousser vers GitHub")
        print("🚀 Render importera automatiquement vos données!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 