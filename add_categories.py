#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour ajouter de nouvelles catégories de véhicules
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_vehicules.settings')
django.setup()

from vehicules.models import CategorieVehicule

def add_new_categories():
    """Ajoute de nouvelles catégories de véhicules"""
    print("🚗 Ajout de nouvelles catégories de véhicules...")
    
    nouvelles_categories = [
        "Bus",
        "Engin de chantier", 
        "Quad",
        "Vélo",
        "Scooter",
        "Bateau",
        "Avion",
        "Hélicoptère"
    ]
    
    added_count = 0
    for nom in nouvelles_categories:
        categorie, created = CategorieVehicule.objects.get_or_create(nom=nom)
        if created:
            print(f"✅ Catégorie ajoutée : {nom}")
            added_count += 1
        else:
            print(f"ℹ️ Catégorie déjà existante : {nom}")
    
    total_categories = CategorieVehicule.objects.count()
    print(f"\n📊 Résumé :")
    print(f"   - {added_count} nouvelles catégories ajoutées")
    print(f"   - {total_categories} catégories au total")
    
    print(f"\n📋 Toutes les catégories disponibles :")
    for cat in CategorieVehicule.objects.all().order_by('nom'):
        print(f"   - {cat.nom}")

if __name__ == "__main__":
    add_new_categories() 