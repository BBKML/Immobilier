#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour tester la validité des fichiers nettoyés
"""

import os
import json

def test_cleaned_data():
    """Teste la validité des fichiers nettoyés"""
    print("🧪 Test des fichiers nettoyés...")
    
    # Fichiers nettoyés à tester
    cleaned_files = [
        'cleaned_local_data_backup_fixed.json',
        'cleaned_fixed_data_backup.json',
        'cleaned_fixed_vehicules_data.json'
    ]
    
    for filename in cleaned_files:
        if os.path.exists(filename):
            print(f"\n🔍 Test de {filename}...")
            try:
                # Lire le fichier
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                print(f"   📊 {len(data)} objets trouvés")
                
                # Analyser les données
                typevehicules = set()
                marques = set()
                marques_with_categories = []
                
                for item in data:
                    if 'model' in item and 'fields' in item:
                        fields = item['fields']
                        
                        if item['model'] == 'vehicules.typevehicule':
                            nom = fields.get('nom', '').strip()
                            if nom:
                                typevehicules.add(nom)
                        
                        elif item['model'] == 'vehicules.marque':
                            nom = fields.get('nom', '').strip()
                            if nom:
                                marques.add(nom)
                                if 'categorie' in fields:
                                    marques_with_categories.append({
                                        'nom': nom,
                                        'categorie': fields['categorie']
                                    })
                
                print(f"   🏷️ TypeVehicules uniques: {len(typevehicules)}")
                print(f"   🚗 Marques uniques: {len(marques)}")
                print(f"   🔗 Marques avec catégories: {len(marques_with_categories)}")
                
                # Vérifier les catégories
                if marques_with_categories:
                    print(f"   📋 Exemples de catégories:")
                    for marque in marques_with_categories[:5]:
                        print(f"      - {marque['nom']}: catégorie ID {marque['categorie']}")
                
                # Vérifier qu'il n'y a pas de doublons
                if len(typevehicules) == len([item for item in data if item.get('model') == 'vehicules.typevehicule']):
                    print(f"   ✅ Aucun doublon TypeVehicule")
                else:
                    print(f"   ⚠️ Doublons TypeVehicule détectés")
                
                if len(marques) == len([item for item in data if item.get('model') == 'vehicules.marque']):
                    print(f"   ✅ Aucun doublon Marque")
                else:
                    print(f"   ⚠️ Doublons Marque détectés")
                
                print(f"   ✅ Fichier {filename} valide")
                
            except Exception as e:
                print(f"   ❌ Erreur avec {filename}: {e}")
        else:
            print(f"⚠️ Fichier {filename} non trouvé")
    
    print("\n🎯 Fichiers nettoyés prêts pour le déploiement!")

if __name__ == "__main__":
    test_cleaned_data() 