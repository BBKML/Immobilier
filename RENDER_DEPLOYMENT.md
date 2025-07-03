# 🚀 Déploiement sur Render

## Configuration du projet

Ce projet est maintenant configuré pour être déployé sur Render.

### Fichiers de configuration créés :

- ✅ `Procfile` - Configuration pour Gunicorn
- ✅ `requirements.txt` - Dépendances Python (avec dj-database-url)
- ✅ `runtime.txt` - Version Python 3.11.18
- ✅ `build.sh` - Script de build automatique
- ✅ `settings.py` - Configuré pour Render

## Étapes de déploiement

### 1. Pousser vers GitHub
```bash
git add .
git commit -m "Configuration pour Render"
git push origin main
```

### 2. Créer un compte Render
- Aller sur https://render.com
- Se connecter avec GitHub

### 3. Créer un nouveau Web Service
- Cliquer sur "New +" > "Web Service"
- Connecter le dépôt GitHub
- Choisir le dépôt `Immobilier`

### 4. Configuration Render
- **Name**: `immobilier-khoa` (ou votre choix)
- **Runtime**: Python
- **Build Command**: `chmod +x build.sh && ./build.sh`
- **Start Command**: `gunicorn gestion_vehicules.wsgi`

### 5. Variables d'environnement
Ajouter dans "Environment Variables" :

```
DEBUG = False
DJANGO_SECRET_KEY = votre_cle_secrete_ici
DATABASE_URL = sqlite:///db.sqlite3
```

### 6. Déployer
- Cliquer sur "Create Web Service"
- Attendre le déploiement (2-3 minutes)

## Après le déploiement

### Créer un superutilisateur
Dans la console Render (Shell) :
```bash
python manage.py shell
```

Dans le shell Django :
```python
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser("admin", "admin@example.com", "admin123")
exit()
```

### Accéder à l'admin
- URL : `https://immobilier-khoa.onrender.com/admin/`
- Username : `admin`
- Password : `admin123`

## Dépannage

### Si l'erreur "no such table: auth_user" apparaît :
1. Aller dans la console Render
2. Exécuter : `python manage.py migrate --run-syncdb`
3. Puis : `python manage.py migrate`

### Si les fichiers statiques ne se chargent pas :
1. Vérifier que `whitenoise` est dans `requirements.txt`
2. Re-déployer l'application

## Support

Pour toute question, vérifiez les logs dans le dashboard Render. 