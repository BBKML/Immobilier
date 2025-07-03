#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour tester la validité finale des fichiers JSON
"""

import os
import json

def test_final_data():
    """Teste la validité finale des fichiers JSON"""
    print("🧪 Test final des fichiers JSON...")
    
    # Fichiers finaux à tester
    final_files = [
        'final_cleaned_local_data_backup_fixed.json',
        'final_cleaned_fixed_data_backup.json',
        'final_cleaned_fixed_vehicules_data.json'
    ]
    
    for filename in final_files:
        if os.path.exists(filename):
            print(f"\n🔍 Test de {filename}...")
            try:
                # Lire le fichier
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                print(f"   📊 {len(data)} objets trouvés")
                
                # Analyser les données
                typevehicules = {}
                marques = set()
                vehicules = []
                motos = []
                
                for item in data:
                    if 'model' in item and 'fields' in item:
                        fields = item['fields']
                        
                        if item['model'] == 'vehicules.typevehicule':
                            pk = item.get('pk')
                            nom = fields.get('nom', '').strip()
                            if pk and nom:
                                typevehicules[pk] = nom
                        
                        elif item['model'] == 'vehicules.marque':
                            nom = fields.get('nom', '').strip()
                            if nom:
                                marques.add(nom)
                        
                        elif item['model'] == 'vehicules.vehicule':
                            vehicules.append({
                                'pk': item.get('pk'),
                                'type_vehicule': fields.get('type_vehicule'),
                                'marque': fields.get('marque')
                            })
                        
                        elif item['model'] == 'vehicules.moto':
                            motos.append({
                                'pk': item.get('pk'),
                                'type_vehicule': fields.get('type_vehicule'),
                                'marque': fields.get('marque')
                            })
                
                print(f"   🏷️ TypeVehicules: {len(typevehicules)}")
                print(f"   🚗 Marques: {len(marques)}")
                print(f"   🚙 Véhicules: {len(vehicules)}")
                print(f"   🏍️ Motos: {len(motos)}")
                
                # Vérifier les références de clés étrangères
                invalid_refs = 0
                
                for vehicule in vehicules:
                    if vehicule['type_vehicule'] not in typevehicules:
                        print(f"   ❌ Véhicule {vehicule['pk']}: type_vehicule {vehicule['type_vehicule']} invalide")
                        invalid_refs += 1
                
                for moto in motos:
                    if moto['type_vehicule'] not in typevehicules:
                        print(f"   ❌ Moto {moto['pk']}: type_vehicule {moto['type_vehicule']} invalide")
                        invalid_refs += 1
                
                if invalid_refs == 0:
                    print(f"   ✅ Toutes les références de clés étrangères sont valides")
                    print(f"   ✅ Fichier {filename} prêt pour l'import!")
                else:
                    print(f"   ⚠️ {invalid_refs} références invalides trouvées")
                
            except Exception as e:
                print(f"   ❌ Erreur avec {filename}: {e}")
        else:
            print(f"⚠️ Fichier {filename} non trouvé")
    
    print("\n🎯 Test final terminé!")

if __name__ == "__main__":
    test_final_data() 