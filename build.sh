#!/usr/bin/env bash
# Script de build pour Render

echo "=== Build process ==="

# Installer les dépendances
pip install -r requirements.txt

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Appliquer les migrations
python manage.py migrate --noinput

echo "=== Build completed ===" 