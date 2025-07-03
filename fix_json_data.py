#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour corriger les fichiers JSON en remplaçant les valeurs de catégorie
par les IDs correspondants dans la nouvelle structure ForeignKey
"""

import os
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_vehicules.settings')
django.setup()

from vehicules.models import CategorieVehicule

def fix_json_files():
    """Corrige les fichiers JSON pour la nouvelle structure"""
    print("🔧 Correction des fichiers JSON pour la nouvelle structure...")
    
    # Mapping des anciennes valeurs vers les IDs des catégories
    categories = {}
    for cat in CategorieVehicule.objects.all():
        if cat.nom == 'Véhicule':
            categories['vehicule'] = cat.id
            categories['voiture'] = cat.id  # Ancienne valeur
        elif cat.nom == 'Moto':
            categories['moto'] = cat.id
    
    print(f"📋 Mapping des catégories: {categories}")
    
    # Fichiers à corriger
    files_to_fix = [
        'local_data_backup.json',
        'data_backup.json', 
        'vehicules_data.json',
        'vehicules_data_fixed.json'
    ]
    
    for filename in files_to_fix:
        if os.path.exists(filename):
            print(f"\n🔄 Traitement de {filename}...")
            try:
                # Lire le fichier
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Compter les modifications
                modified_count = 0
                
                # Parcourir tous les objets
                for item in data:
                    if 'model' in item and 'fields' in item:
                        # Si c'est une marque avec une catégorie
                        if item['model'] == 'vehicules.marque' and 'categorie' in item['fields']:
                            old_value = item['fields']['categorie']
                            if old_value in categories:
                                item['fields']['categorie'] = categories[old_value]
                                modified_count += 1
                                print(f"   ✅ Marque '{item['fields'].get('nom', 'N/A')}': {old_value} -> ID {categories[old_value]}")
                            else:
                                print(f"   ⚠️ Catégorie inconnue '{old_value}' pour la marque '{item['fields'].get('nom', 'N/A')}'")
                
                # Sauvegarder le fichier corrigé
                fixed_filename = f"fixed_{filename}"
                with open(fixed_filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                print(f"✅ {modified_count} modifications dans {filename} -> {fixed_filename}")
                
            except Exception as e:
                print(f"❌ Erreur lors du traitement de {filename}: {e}")
        else:
            print(f"⚠️ Fichier {filename} non trouvé")
    
    print("\n🎉 Correction terminée!")
    print("\n📝 Fichiers corrigés créés:")
    for filename in files_to_fix:
        fixed_filename = f"fixed_{filename}"
        if os.path.exists(fixed_filename):
            print(f"   - {fixed_filename}")

if __name__ == "__main__":
    fix_json_files() 