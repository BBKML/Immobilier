#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour nettoyer et corriger les données JSON avant import
Résout les problèmes de contraintes UNIQUE et NOT NULL
"""

import os
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_vehicules.settings')
django.setup()

from vehicules.models import CategorieVehicule

def clean_and_fix_data():
    """Nettoie et corrige les données JSON"""
    print("🧹 Nettoyage et correction des données JSON...")
    
    # Mapping des catégories
    categories = {}
    for cat in CategorieVehicule.objects.all():
        if cat.nom == 'Véhicule':
            categories['vehicule'] = cat.id
            categories['voiture'] = cat.id
        elif cat.nom == 'Moto':
            categories['moto'] = cat.id
    
    print(f"📋 Mapping des catégories: {categories}")
    
    # Fichiers à traiter
    files_to_process = [
        'local_data_backup_fixed.json',
        'fixed_data_backup.json',
        'fixed_vehicules_data.json'
    ]
    
    for filename in files_to_process:
        if os.path.exists(filename):
            print(f"\n🔄 Traitement de {filename}...")
            try:
                # Lire le fichier
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Nettoyer les données
                cleaned_data = []
                seen_typevehicules = set()
                seen_marques = set()
                
                for item in data:
                    if 'model' in item and 'fields' in item:
                        fields = item['fields']
                        
                        # Traitement des TypeVehicule (éviter les doublons)
                        if item['model'] == 'vehicules.typevehicule':
                            nom = fields.get('nom', '').strip()
                            if nom and nom not in seen_typevehicules:
                                seen_typevehicules.add(nom)
                                cleaned_data.append(item)
                            else:
                                print(f"   🗑️ TypeVehicule en double ignoré: {nom}")
                        
                        # Traitement des Marques (ajouter catégorie si manquante)
                        elif item['model'] == 'vehicules.marque':
                            nom = fields.get('nom', '').strip()
                            if nom and nom not in seen_marques:
                                seen_marques.add(nom)
                                
                                # S'assurer qu'une catégorie est assignée
                                if 'categorie' not in fields or not fields['categorie']:
                                    # Assigner une catégorie par défaut (Véhicule)
                                    fields['categorie'] = categories['vehicule']
                                    print(f"   ✅ Marque '{nom}': catégorie par défaut assignée (ID {categories['vehicule']})")
                                elif isinstance(fields['categorie'], str):
                                    # Convertir la chaîne en ID
                                    if fields['categorie'] in categories:
                                        fields['categorie'] = categories[fields['categorie']]
                                        print(f"   ✅ Marque '{nom}': {fields['categorie']} -> ID {categories[fields['categorie']]}")
                                    else:
                                        # Catégorie inconnue, assigner par défaut
                                        fields['categorie'] = categories['vehicule']
                                        print(f"   ⚠️ Marque '{nom}': catégorie inconnue '{fields['categorie']}', assignée par défaut")
                                
                                cleaned_data.append(item)
                            else:
                                print(f"   🗑️ Marque en double ignorée: {nom}")
                        
                        # Autres modèles (pas de traitement spécial)
                        else:
                            cleaned_data.append(item)
                
                # Sauvegarder le fichier nettoyé
                cleaned_filename = f"cleaned_{filename}"
                with open(cleaned_filename, 'w', encoding='utf-8') as f:
                    json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
                
                print(f"✅ {len(cleaned_data)} objets nettoyés -> {cleaned_filename}")
                print(f"   📊 TypeVehicules uniques: {len(seen_typevehicules)}")
                print(f"   📊 Marques uniques: {len(seen_marques)}")
                
            except Exception as e:
                print(f"❌ Erreur lors du traitement de {filename}: {e}")
        else:
            print(f"⚠️ Fichier {filename} non trouvé")
    
    print("\n🎉 Nettoyage terminé!")
    print("\n📝 Fichiers nettoyés créés:")
    for filename in files_to_process:
        cleaned_filename = f"cleaned_{filename}"
        if os.path.exists(cleaned_filename):
            print(f"   - {cleaned_filename}")

if __name__ == "__main__":
    clean_and_fix_data() 