#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier l'encodage des fichiers JSON
et diagnostiquer les problèmes d'encodage sur Render
"""

import os
import json
import chardet
import sys
from pathlib import Path

def detect_encoding(file_path):
    """Détecte l'encodage d'un fichier"""
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            return result
    except Exception as e:
        return {'encoding': None, 'confidence': 0, 'error': str(e)}

def test_json_file(file_path):
    """Teste un fichier JSON pour les problèmes d'encodage"""
    print(f"\n🔍 Test du fichier: {file_path}")
    print("=" * 50)
    
    if not os.path.exists(file_path):
        print(f"❌ Fichier non trouvé: {file_path}")
        return False
    
    # Détecter l'encodage
    encoding_info = detect_encoding(file_path)
    print(f"📊 Détection d'encodage: {encoding_info}")
    
    # Tester différents encodages
    encodings_to_test = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings_to_test:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
                data = json.loads(content)
                print(f"✅ Succès avec encodage: {encoding}")
                print(f"   📈 Nombre d'objets: {len(data)}")
                return True
        except UnicodeDecodeError as e:
            print(f"❌ Erreur de décodage avec {encoding}: {e}")
        except json.JSONDecodeError as e:
            print(f"❌ Erreur JSON avec {encoding}: {e}")
        except Exception as e:
            print(f"❌ Erreur inattendue avec {encoding}: {e}")
    
    return False

def create_test_json():
    """Crée un fichier JSON de test avec encodage UTF-8 explicite"""
    test_data = [
        {
            "model": "vehicules.client",
            "pk": 1,
            "fields": {
                "nom": "TEST CLIENT",
                "contact": "123456789",
                "adresse": "Adresse de test"
            }
        },
        {
            "model": "vehicules.vehicule",
            "pk": 1,
            "fields": {
                "immatriculation": "TEST123",
                "marque": 1,
                "modele": "Test Modèle",
                "annee": 2020,
                "prix": 15000.00
            }
        }
    ]
    
    # Sauvegarder avec encodage UTF-8 explicite
    with open('test_encoding.json', 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    print("✅ Fichier de test créé: test_encoding.json")

def main():
    """Fonction principale"""
    print("🔧 DIAGNOSTIC D'ENCODAGE JSON")
    print("=" * 60)
    
    # Créer un fichier de test
    create_test_json()
    
    # Tester les fichiers existants
    files_to_test = [
        'data_backup.json',
        'local_data_backup.json',
        'vehicules_data.json',
        'test_encoding.json'
    ]
    
    success_count = 0
    for file_path in files_to_test:
        if test_json_file(file_path):
            success_count += 1
    
    print(f"\n📊 RÉSULTATS: {success_count}/{len(files_to_test)} fichiers valides")
    
    if success_count == 0:
        print("\n🚨 Aucun fichier JSON valide trouvé!")
        print("💡 Solutions possibles:")
        print("   1. Vérifier l'encodage des fichiers source")
        print("   2. Recréer les fichiers avec encodage UTF-8")
        print("   3. Utiliser les données de fallback")
    else:
        print(f"\n✅ {success_count} fichier(s) JSON valide(s) trouvé(s)")

if __name__ == "__main__":
    main() 