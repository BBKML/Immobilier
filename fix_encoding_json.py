#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour corriger l'encodage du fichier local_data_backup.json
"""

import json
import chardet

def fix_encoding():
    """Corrige l'encodage du fichier local_data_backup.json"""
    print("🔧 Correction de l'encodage de local_data_backup.json...")
    
    try:
        # Détecter l'encodage
        with open('local_data_backup.json', 'rb') as f:
            raw_data = f.read()
            detected = chardet.detect(raw_data)
            encoding = detected['encoding']
            confidence = detected['confidence']
        
        print(f"📋 Encodage détecté: {encoding} (confiance: {confidence:.2f})")
        
        # Lire avec l'encodage détecté
        with open('local_data_backup.json', 'r', encoding=encoding) as f:
            data = json.load(f)
        
        # Sauvegarder en UTF-8
        with open('local_data_backup_fixed.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print("✅ Fichier corrigé: local_data_backup_fixed.json")
        
        # Maintenant corriger les catégories
        import os
        import django
        
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_vehicules.settings')
        django.setup()
        
        from vehicules.models import CategorieVehicule
        
        categories = {}
        for cat in CategorieVehicule.objects.all():
            if cat.nom == 'Véhicule':
                categories['vehicule'] = cat.id
                categories['voiture'] = cat.id
            elif cat.nom == 'Moto':
                categories['moto'] = cat.id
        
        print(f"📋 Mapping des catégories: {categories}")
        
        # Corriger les catégories
        modified_count = 0
        for item in data:
            if 'model' in item and 'fields' in item:
                if item['model'] == 'vehicules.marque' and 'categorie' in item['fields']:
                    old_value = item['fields']['categorie']
                    if old_value in categories:
                        item['fields']['categorie'] = categories[old_value]
                        modified_count += 1
                        print(f"   ✅ Marque '{item['fields'].get('nom', 'N/A')}': {old_value} -> ID {categories[old_value]}")
        
        # Sauvegarder le fichier final
        with open('local_data_backup_fixed.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ {modified_count} modifications appliquées")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    fix_encoding() 