#!/usr/bin/env bash
# Script de migration manuel pour résoudre les problèmes de base de données

echo "=== Script de migration manuel ==="

echo "1. Vérification de la connexion à la base de données..."
python manage.py check --database default

echo "2. Affichage du statut des migrations..."
python manage.py showmigrations

echo "3. Application des migrations..."
python manage.py migrate --no-input --verbosity=2

echo "4. Vérification finale des migrations..."
python manage.py showmigrations --verbosity=2

echo "5. Test de la base de données..."
python manage.py shell << END
from django.db import connection
from vehicules.models import Vehicule, Moto, Client, Proprietaire, Marque

# Test de connexion
with connection.cursor() as cursor:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables existantes:")
    for table in tables:
        print(f"  - {table[0]}")

# Test des modèles
try:
    vehicule_count = Vehicule.objects.count()
    moto_count = Moto.objects.count()
    client_count = Client.objects.count()
    proprietaire_count = Proprietaire.objects.count()
    marque_count = Marque.objects.count()
    
    print(f"\nNombre d'objets dans la base:")
    print(f"  - Véhicules: {vehicule_count}")
    print(f"  - Motos: {moto_count}")
    print(f"  - Clients: {client_count}")
    print(f"  - Propriétaires: {proprietaire_count}")
    print(f"  - Marques: {marque_count}")
    
    print("\n✅ Base de données fonctionnelle!")
except Exception as e:
    print(f"\n❌ Erreur lors du test: {e}")
END

echo "=== Script terminé ===" 