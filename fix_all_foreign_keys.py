#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour corriger TOUTES les références de clés étrangères
- Corrige les références marque_id pour les motos et véhicules
- Corrige les références type_vehicule pour les véhicules
- Supprime le champ type_vehicule des motos
"""

import os
import json

def fix_all_foreign_keys(filename):
    """Corrige toutes les références de clés étrangères"""
    print(f"🔧 Correction de {filename}...")
    
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Récupérer tous les IDs valides
    typevehicules = {item["pk"] for item in data if item.get("model") == "vehicules.typevehicule"}
    marques = {item["pk"] for item in data if item.get("model") == "vehicules.marque"}
    
    fallback_type_id = min(typevehicules) if typevehicules else None
    fallback_marque_id = min(marques) if marques else None
    
    print(f"   TypeVehicules: {typevehicules}")
    print(f"   Marques: {marques}")

    fixed_count = 0
    
    for item in data:
        if item.get("model") == "vehicules.vehicule":
            fields = item["fields"]
            
            # Corriger type_vehicule
            if "type_vehicule" in fields and fields["type_vehicule"] not in typevehicules:
                fields["type_vehicule"] = fallback_type_id
                fixed_count += 1
            
            # Corriger marque
            if "marque" in fields and fields["marque"] not in marques:
                fields["marque"] = fallback_marque_id
                fixed_count += 1
                
        elif item.get("model") == "vehicules.moto":
            fields = item["fields"]
            
            # Supprimer type_vehicule des motos
            if "type_vehicule" in fields:
                del fields["type_vehicule"]
                fixed_count += 1
            
            # Corriger marque
            if "marque" in fields and fields["marque"] not in marques:
                fields["marque"] = fallback_marque_id
                fixed_count += 1

    # Sauvegarder
    fixed_name = "render_ready_" + filename
    with open(fixed_name, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"   ✅ {fixed_count} corrections -> {fixed_name}")

def main():
    """Fonction principale"""
    print("🚀 Correction complète des clés étrangères...")
    
    files_to_fix = [
        "deployable_final_cleaned_local_data_backup_fixed.json",
        "deployable_final_cleaned_fixed_data_backup.json",
        "deployable_final_cleaned_fixed_vehicules_data.json"
    ]
    
    for filename in files_to_fix:
        if os.path.exists(filename):
            fix_all_foreign_keys(filename)
        else:
            print(f"⚠️ {filename} non trouvé")
    
    print("\n🎉 Correction terminée!")
    print("\n📝 Fichiers prêts pour Render:")
    for filename in files_to_fix:
        render_ready_name = "render_ready_" + filename
        if os.path.exists(render_ready_name):
            print(f"   - {render_ready_name}")

if __name__ == "__main__":
    main() 