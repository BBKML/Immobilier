#!/usr/bin/env bash
# Script de build pour Render

echo "=== Build process ==="

# Installer les dépendances
pip install -r requirements.txt

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Appliquer les migrations
python manage.py migrate --noinput

# Créer un superuser par défaut (seulement si aucun superuser n'existe)
python manage.py create_superuser

echo "=== Build completed ===" 