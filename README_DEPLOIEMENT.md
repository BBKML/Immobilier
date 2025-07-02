# Guide de Déploiement - Gestion Véhicules

## 🚀 Prérequis

- Python 3.8+
- Serveur web (Apache/Nginx)
- Base de données (SQLite pour commencer, PostgreSQL recommandé pour la production)
- Certificat SSL

## 📋 Installation

### 1. Cloner le projet
```bash
git clone [URL_DU_REPO]
cd Immobilier
```

### 2. Créer l'environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration des variables d'environnement
Créer un fichier `.env` à la racine du projet :
```env
DJANGO_SECRET_KEY=votre-cle-secrete-tres-longue-et-aleatoire
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com
```

### 5. Migrations et collecte des statiques
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### 6. Créer un superutilisateur
```bash
python manage.py createsuperuser
```

## 🔒 Sécurité

### Générer une clé secrète sécurisée
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Configuration SSL/HTTPS
- Installer un certificat SSL (Let's Encrypt recommandé)
- Configurer le serveur web pour rediriger HTTP vers HTTPS
- Les paramètres de sécurité sont automatiquement activés quand `DEBUG=False`

## 🗄️ Base de données

### SQLite (développement)
Aucune configuration supplémentaire nécessaire.

### PostgreSQL (production recommandé)
```bash
pip install psycopg2-binary
```

Modifier `settings.py` :
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nom_db',
        'USER': 'utilisateur_db',
        'PASSWORD': 'mot_de_passe_db',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🌐 Serveur Web

### Apache avec mod_wsgi
```apache
<VirtualHost *:80>
    ServerName votre-domaine.com
    Redirect permanent / https://votre-domaine.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName votre-domaine.com
    
    SSLEngine on
    SSLCertificateFile /path/to/cert.pem
    SSLCertificateKeyFile /path/to/key.pem
    
    Alias /static/ /path/to/staticfiles/
    <Directory /path/to/staticfiles>
        Require all granted
    </Directory>
    
    WSGIDaemonProcess gestion_vehicules python-path=/path/to/project:/path/to/venv/lib/python3.8/site-packages
    WSGIProcessGroup gestion_vehicules
    WSGIScriptAlias / /path/to/project/gestion_vehicules/wsgi.py
    
    <Directory /path/to/project>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
</VirtualHost>
```

### Nginx + Gunicorn
```nginx
server {
    listen 80;
    server_name votre-domaine.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name votre-domaine.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location /static/ {
        alias /path/to/staticfiles/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📊 Sauvegarde

### Script de sauvegarde automatique
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/path/to/backups"

# Sauvegarde de la base de données
python manage.py dumpdata > $BACKUP_DIR/db_backup_$DATE.json

# Sauvegarde des fichiers média (si applicable)
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz media/

# Nettoyage des anciennes sauvegardes (garder 30 jours)
find $BACKUP_DIR -name "*.json" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

## 🔧 Maintenance

### Mises à jour
```bash
# Arrêter le serveur
sudo systemctl stop apache2  # ou nginx

# Mettre à jour le code
git pull origin main

# Installer les nouvelles dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Collecter les statiques
python manage.py collectstatic --noinput

# Redémarrer le serveur
sudo systemctl start apache2  # ou nginx
```

### Surveillance
- Surveiller les logs : `/var/log/apache2/` ou `/var/log/nginx/`
- Surveiller l'espace disque
- Surveiller les performances de la base de données

## 📞 Support

En cas de problème :
1. Vérifier les logs d'erreur
2. Vérifier la configuration des variables d'environnement
3. Vérifier les permissions des fichiers
4. Contacter le développeur avec les logs d'erreur

## ✅ Checklist de déploiement

- [ ] Variables d'environnement configurées
- [ ] DEBUG = False
- [ ] Clé secrète sécurisée
- [ ] SSL/HTTPS configuré
- [ ] Base de données configurée
- [ ] Migrations appliquées
- [ ] Statiques collectées
- [ ] Superutilisateur créé
- [ ] Sauvegardes configurées
- [ ] Monitoring en place 