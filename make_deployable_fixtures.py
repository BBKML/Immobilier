#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script final pour créer des fixtures déployables
- Supprime le champ type_vehicule des motos (n'existe pas dans le modèle)
- Corrige les références de clés étrangères pour les véhicules
"""

import os
import json

def fix_final_json(filename):
    """Corrige un fichier JSON pour le rendre déployable"""
    print(f"🔄 Traitement de {filename}...")
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Récupérer tous les typevehicule valides
        typevehicules = {item["pk"] for item in data if item.get("model") == "vehicules.typevehicule"}
        fallback_id = min(typevehicules) if typevehicules else None
        
        print(f"   📋 TypeVehicules valides: {typevehicules}")
        print(f"   🎯 ID de fallback: {fallback_id}")

        fixed_count = 0
        removed_count = 0
        
        for item in data:
            if item.get("model") == "vehicules.vehicule":
                fields = item["fields"]
                if "type_vehicule" in fields and fields["type_vehicule"] not in typevehicules:
                    print(f"   🔄 Véhicule {item.get('pk')}: type_vehicule {fields['type_vehicule']} -> {fallback_id}")
                    fields["type_vehicule"] = fallback_id
                    fixed_count += 1
                    
            elif item.get("model") == "vehicules.moto":
                fields = item["fields"]
                if "type_vehicule" in fields:
                    print(f"   🗑️ Moto {item.get('pk')}: suppression du champ type_vehicule")
                    del fields["type_vehicule"]
                    removed_count += 1

        # Sauvegarder le fichier corrigé
        fixed_name = "deployable_" + filename
        with open(fixed_name, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"   ✅ {fixed_count} références corrigées, {removed_count} champs supprimés")
        print(f"   📁 Fichier corrigé : {fixed_name}")
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")

def main():
    """Fonction principale"""
    print("🚀 Création des fixtures déployables...")
    
    # Fichiers à corriger
    files_to_fix = [
        "final_cleaned_local_data_backup_fixed.json",
        "final_cleaned_fixed_data_backup.json",
        "final_cleaned_fixed_vehicules_data.json"
    ]
    
    for filename in files_to_fix:
        if os.path.exists(filename):
            fix_final_json(filename)
        else:
            print(f"⚠️ Fichier {filename} non trouvé")
    
    print("\n🎉 Fixtures déployables créées!")
    print("\n📝 Fichiers prêts pour le déploiement:")
    for filename in files_to_fix:
        deployable_name = "deployable_" + filename
        if os.path.exists(deployable_name):
            print(f"   - {deployable_name}")

if __name__ == "__main__":
    main() 