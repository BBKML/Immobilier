#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour corriger les problèmes d'encodage des fichiers JSON
en les convertissant en UTF-8
"""

import os
import json
import chardet
import shutil
from pathlib import Path

def fix_json_encoding(input_file, output_file=None):
    """Corrige l'encodage d'un fichier JSON"""
    if output_file is None:
        output_file = input_file.replace('.json', '_fixed.json')
    
    print(f"🔧 Correction de l'encodage: {input_file} -> {output_file}")
    
    try:
        # Détecter l'encodage
        with open(input_file, 'rb') as f:
            raw_data = f.read()
            detected = chardet.detect(raw_data)
            print(f"📊 Encodage détecté: {detected}")
        
        # Essayer de décoder avec l'encodage détecté
        encoding = detected['encoding']
        if encoding:
            try:
                content = raw_data.decode(encoding)
                data = json.loads(content)
                print(f"✅ Décodage réussi avec {encoding}")
            except (UnicodeDecodeError, json.JSONDecodeError):
                # Essayer d'autres encodages
                for fallback_encoding in ['latin-1', 'cp1252', 'iso-8859-1']:
                    try:
                        content = raw_data.decode(fallback_encoding)
                        data = json.loads(content)
                        encoding = fallback_encoding
                        print(f"✅ Décodage réussi avec {fallback_encoding}")
                        break
                    except (UnicodeDecodeError, json.JSONDecodeError):
                        continue
                else:
                    print(f"❌ Impossible de décoder le fichier {input_file}")
                    return False
        else:
            print(f"❌ Impossible de détecter l'encodage de {input_file}")
            return False
        
        # Sauvegarder avec encodage UTF-8
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Fichier corrigé sauvegardé: {output_file}")
        print(f"📈 Nombre d'objets: {len(data)}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
        return False

def create_clean_backup():
    """Crée une sauvegarde propre avec encodage UTF-8"""
    print("\n🔄 Création d'une sauvegarde propre...")
    
    # Utiliser Django pour créer une sauvegarde propre
    try:
        import os
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_vehicules.settings')
        
        import django
        django.setup()
        
        from django.core.management import call_command
        from django.core.management.base import CommandError
        
        # Créer une sauvegarde propre
        output_file = 'clean_data_backup.json'
        call_command('dumpdata', 'vehicules', 
                    output=output_file, 
                    indent=2, 
                    natural_foreign=True,
                    natural_primary=True)
        
        print(f"✅ Sauvegarde propre créée: {output_file}")
        
        # Vérifier le fichier
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"📈 Nombre d'objets dans la sauvegarde: {len(data)}")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de la sauvegarde: {e}")
        return None

def main():
    """Fonction principale"""
    print("🔧 CORRECTION D'ENCODAGE JSON")
    print("=" * 60)
    
    # Fichiers à corriger
    files_to_fix = [
        'data_backup.json',
        'local_data_backup.json',
        'vehicules_data.json'
    ]
    
    fixed_files = []
    
    # Corriger les fichiers existants
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            if fix_json_encoding(file_path):
                fixed_files.append(file_path.replace('.json', '_fixed.json'))
    
    # Créer une sauvegarde propre
    clean_backup = create_clean_backup()
    if clean_backup:
        fixed_files.append(clean_backup)
    
    print(f"\n📊 RÉSULTATS: {len(fixed_files)} fichier(s) corrigé(s)")
    
    if fixed_files:
        print("\n✅ Fichiers corrigés:")
        for file_path in fixed_files:
            print(f"   📄 {file_path}")
        
        print("\n💡 Prochaines étapes:")
        print("   1. Remplacer les anciens fichiers par les versions corrigées")
        print("   2. Pousser les changements vers GitHub")
        print("   3. Redéployer sur Render")
    else:
        print("\n🚨 Aucun fichier corrigé!")

if __name__ == "__main__":
    main() 