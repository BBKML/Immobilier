#!/usr/bin/env bash
# Script pour forcer l'application des migrations sur Render

echo "=== FORCE MIGRATION SCRIPT ==="

echo "1. Vérification de l'environnement..."
echo "   - Python version: $(python --version)"
echo "   - Django version: $(python -c 'import django; print(django.get_version())')"
echo "   - Working directory: $(pwd)"

echo "2. Vérification de la base de données..."
python manage.py check --database default

echo "3. Affichage du statut des migrations..."
python manage.py showmigrations

echo "4. Suppression de la base de données existante (si elle existe)..."
if [ -f "db.sqlite3" ]; then
    echo "   - Suppression de db.sqlite3"
    rm db.sqlite3
else
    echo "   - Aucune base de données existante trouvée"
fi

echo "5. Création d'une nouvelle base de données..."
python manage.py migrate --run-syncdb

echo "6. Application de toutes les migrations..."
python manage.py migrate --no-input --verbosity=2

echo "7. Vérification finale des migrations..."
python manage.py showmigrations --verbosity=2

echo "8. Test de la base de données..."
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

echo "9. Création du superuser..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "admin123")
    print("✅ Superuser 'admin' créé avec succès!")
else:
    print("ℹ️  Superuser 'admin' existe déjà")
END

echo "=== SCRIPT TERMINÉ ===" 