#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour corriger les références de clés étrangères dans les fichiers JSON
Résout les problèmes de références invalides après nettoyage
"""

import os
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_vehicules.settings')
django.setup()

def fix_foreign_keys():
    """Corrige les références de clés étrangères"""
    print("🔧 Correction des clés étrangères...")
    
    # Fichiers à traiter
    files_to_process = [
        'cleaned_local_data_backup_fixed.json',
        'cleaned_fixed_data_backup.json',
        'cleaned_fixed_vehicules_data.json'
    ]
    
    for filename in files_to_process:
        if os.path.exists(filename):
            print(f"\n🔄 Traitement de {filename}...")
            try:
                # Lire le fichier
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Analyser les TypeVehicule disponibles
                typevehicules = {}
                for item in data:
                    if item.get('model') == 'vehicules.typevehicule':
                        pk = item.get('pk')
                        nom = item['fields'].get('nom', '').strip()
                        if pk and nom:
                            typevehicules[pk] = nom
                
                print(f"   📋 TypeVehicules disponibles: {typevehicules}")
                
                # Créer un mapping des anciens IDs vers les nouveaux
                # On va utiliser le premier TypeVehicule disponible comme fallback
                fallback_id = min(typevehicules.keys()) if typevehicules else None
                
                # Corriger les références dans les véhicules
                fixed_count = 0
                for item in data:
                    if item.get('model') == 'vehicules.vehicule':
                        fields = item['fields']
                        if 'type_vehicule' in fields:
                            old_type_id = fields['type_vehicule']
                            if old_type_id not in typevehicules:
                                # Référence invalide, utiliser le fallback
                                if fallback_id:
                                    fields['type_vehicule'] = fallback_id
                                    fixed_count += 1
                                    print(f"   🔄 Véhicule {item.get('pk', 'N/A')}: type_vehicule {old_type_id} -> {fallback_id}")
                                else:
                                    print(f"   ⚠️ Aucun TypeVehicule disponible pour le véhicule {item.get('pk', 'N/A')}")
                
                # Corriger les références dans les motos
                for item in data:
                    if item.get('model') == 'vehicules.moto':
                        fields = item['fields']
                        if 'type_vehicule' in fields:
                            old_type_id = fields['type_vehicule']
                            if old_type_id is None or old_type_id not in typevehicules:
                                # Référence invalide ou manquante, utiliser le fallback
                                if fallback_id:
                                    fields['type_vehicule'] = fallback_id
                                    fixed_count += 1
                                    print(f"   🔄 Moto {item.get('pk', 'N/A')}: type_vehicule {old_type_id} -> {fallback_id}")
                                else:
                                    print(f"   ⚠️ Aucun TypeVehicule disponible pour la moto {item.get('pk', 'N/A')}")
                        else:
                            # Ajouter type_vehicule s'il manque
                            if fallback_id:
                                fields['type_vehicule'] = fallback_id
                                fixed_count += 1
                                print(f"   ➕ Moto {item.get('pk', 'N/A')}: type_vehicule ajouté -> {fallback_id}")
                
                # Sauvegarder le fichier corrigé
                fixed_filename = f"final_{filename}"
                with open(fixed_filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                print(f"✅ {fixed_count} références corrigées -> {fixed_filename}")
                
            except Exception as e:
                print(f"❌ Erreur lors du traitement de {filename}: {e}")
        else:
            print(f"⚠️ Fichier {filename} non trouvé")
    
    print("\n🎉 Correction des clés étrangères terminée!")
    print("\n📝 Fichiers finaux créés:")
    for filename in files_to_process:
        final_filename = f"final_{filename}"
        if os.path.exists(final_filename):
            print(f"   - {final_filename}")

if __name__ == "__main__":
    fix_foreign_keys() 