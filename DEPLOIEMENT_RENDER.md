# 🚀 Déploiement sur Render - Gestion Véhicules

## 📋 Prérequis

- Compte Render.com (gratuit)
- Code source sur GitHub/GitLab
- 5 minutes de configuration

## 🔧 Configuration automatique

### 1. Préparer le repository

Votre projet contient déjà tous les fichiers nécessaires :
- ✅ `render.yaml` - Configuration automatique
- ✅ `requirements.txt` - Dépendances avec gunicorn et whitenoise
- ✅ `build.sh` - Script de build
- ✅ Configuration Django optimisée pour Render

### 2. Déployer sur Render

#### Option A : Déploiement automatique (Recommandé)

1. **Connectez votre repository**
   - Allez sur [render.com](https://render.com)
   - Cliquez "New +" → "Web Service"
   - Connectez votre compte GitHub/GitLab
   - Sélectionnez votre repository

2. **Configuration automatique**
   - Render détectera automatiquement le fichier `render.yaml`
   - Cliquez "Create Web Service"
   - Le déploiement se lance automatiquement

#### Option B : Configuration manuelle

Si vous préférez configurer manuellement :

1. **Créer un Web Service**
   - Name: `gestion-vehicules`
   - Environment: `Python 3`
   - Build Command: `./build.sh`
   - Start Command: `gunicorn gestion_vehicules.wsgi:application`

2. **Variables d'environnement**
   - `DJANGO_DEBUG`: `False`
   - `DJANGO_ALLOWED_HOSTS`: `.onrender.com`
   - `DJANGO_SECRET_KEY`: (généré automatiquement par Render)

## 🔒 Sécurité

### Variables d'environnement automatiques
Render configure automatiquement :
- ✅ Clé secrète sécurisée
- ✅ HTTPS/SSL
- ✅ Variables de sécurité Django
- ✅ Fichiers statiques optimisés

### Base de données
Pour la production, ajoutez une base de données PostgreSQL :

1. **Créer une base de données**
   - "New +" → "PostgreSQL"
   - Plan: Free (pour commencer)
   - Nom: `gestion-vehicules-db`

2. **Connecter à l'application**
   - Dans votre Web Service
   - "Environment" → "Add Environment Variable"
   - Ajoutez les variables de base de données fournies par Render

3. **Mettre à jour settings.py**
   ```python
   import os
   import dj_database_url
   
   DATABASES = {
       'default': dj_database_url.config(
           default=os.environ.get('DATABASE_URL'),
           conn_max_age=600
       )
   }
   ```

## 📊 Monitoring

### Logs automatiques
- Render fournit des logs en temps réel
- Accès via le dashboard Render
- Alertes automatiques en cas d'erreur

### Health Check
- URL de vérification : `/admin/`
- Render vérifie automatiquement la santé de l'application
- Redémarrage automatique en cas de problème

## 🔄 Mises à jour

### Déploiement automatique
- Chaque push sur la branche principale déclenche un redéploiement
- Pas d'intervention manuelle nécessaire
- Rollback automatique en cas d'erreur

### Déploiement manuel
- Via le dashboard Render
- Possibilité de déployer une branche spécifique
- Historique des déploiements

## 💰 Coûts

### Plan gratuit
- ✅ 750 heures/mois
- ✅ 512 MB RAM
- ✅ Base de données PostgreSQL incluse
- ✅ SSL/HTTPS gratuit
- ✅ Domaine personnalisé possible

### Plans payants
- À partir de $7/mois pour plus de ressources
- Recommandé pour une utilisation intensive

## 🚀 Première connexion

1. **Attendre le déploiement**
   - 2-3 minutes pour le premier déploiement
   - URL : `https://votre-app.onrender.com`

2. **Créer un superutilisateur**
   ```bash
   # Via le dashboard Render
   # "Shell" → Exécuter :
   python manage.py createsuperuser
   ```

3. **Accéder à l'application**
   - URL : `https://votre-app.onrender.com/admin/`
   - Connectez-vous avec vos identifiants

## 🔧 Personnalisation

### Domaine personnalisé
1. Achetez un domaine (ex: `gestion-vehicules.com`)
2. Dans Render : "Settings" → "Custom Domains"
3. Ajoutez votre domaine
4. Configurez les DNS selon les instructions

### Variables d'environnement supplémentaires
```bash
# Pour les emails
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-app

# Pour les sauvegardes
BACKUP_ENABLED=True
BACKUP_SCHEDULE=0 2 * * *  # Tous les jours à 2h du matin
```

## 🆘 Support

### Problèmes courants

1. **Erreur de build**
   - Vérifiez les logs dans Render
   - Assurez-vous que `requirements.txt` est à jour

2. **Erreur 500**
   - Vérifiez les variables d'environnement
   - Consultez les logs d'application

3. **Fichiers statiques non trouvés**
   - Vérifiez que `build.sh` s'exécute correctement
   - Assurez-vous que whitenoise est configuré

### Ressources
- [Documentation Render](https://render.com/docs)
- [Support Render](https://render.com/support)
- [Forum communautaire](https://community.render.com)

## ✅ Checklist de déploiement

- [ ] Repository connecté à Render
- [ ] Déploiement automatique activé
- [ ] Variables d'environnement configurées
- [ ] Base de données créée (optionnel)
- [ ] Superutilisateur créé
- [ ] Application accessible via HTTPS
- [ ] Tests de fonctionnalités effectués
- [ ] Domaine personnalisé configuré (optionnel)

---

**Temps de déploiement estimé** : 5-10 minutes  
**Coût mensuel** : Gratuit (plan de base)  
**Support** : Documentation Render + Support communautaire 