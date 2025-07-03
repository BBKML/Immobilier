# 🚗 Gestion Véhicules - Application Django

Application de gestion de véhicules et motos avec interface d'administration moderne.

## ✨ Fonctionnalités

- **Gestion complète des véhicules** : Ajout, modification, suppression
- **Gestion des motos** : Catalogue et suivi des motos
- **Gestion des clients** : Base de données clients
- **Interface d'administration moderne** : Jazzmin UI
- **Export de données** : Excel et PDF
- **Historique des modifications** : Simple History
- **Interface responsive** : Compatible mobile et desktop

## 🛠️ Technologies

- **Backend** : Django 5.2.3
- **Interface Admin** : Django Jazzmin
- **Base de données** : SQLite (développement) / PostgreSQL (production)
- **Serveur** : Gunicorn
- **Fichiers statiques** : WhiteNoise
- **Export** : OpenPyXL (Excel), ReportLab (PDF)

## 🚀 Installation locale

### Prérequis
- Python 3.11+
- pip

### Installation

1. **Cloner le projet**
   ```bash
   git clone https://github.com/BBKML/Immobilier.git
   cd Immobilier
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer la base de données**
   ```bash
   python manage.py migrate
   ```

5. **Créer un superutilisateur**
   ```bash
   python manage.py createsuperuser
   ```

6. **Lancer le serveur**
   ```bash
   python manage.py runserver
   ```

7. **Accéder à l'application**
   - Site : http://127.0.0.1:8000/
   - Admin : http://127.0.0.1:8000/admin/

## 🌐 Déploiement sur Render

Le projet est configuré pour être déployé sur Render.

### Configuration automatique
- **Procfile** : Configuration Gunicorn
- **requirements.txt** : Dépendances Python
- **runtime.txt** : Version Python 3.11.18
- **build.sh** : Script de build automatique

### Variables d'environnement Render
```
DEBUG = False
DJANGO_SECRET_KEY = votre_cle_secrete
DATABASE_URL = sqlite:///db.sqlite3
```

### Déploiement
1. Connecter le dépôt GitHub à Render
2. Configurer les variables d'environnement
3. Déployer automatiquement

## 📁 Structure du projet

```
Immobilier/
├── gestion_vehicules/     # Configuration Django
│   ├── settings.py       # Paramètres du projet
│   ├── urls.py          # URLs principales
│   └── wsgi.py          # Configuration WSGI
├── vehicules/            # Application principale
│   ├── models.py        # Modèles de données
│   ├── admin.py         # Interface d'administration
│   └── views.py         # Vues de l'application
├── static/              # Fichiers statiques
├── templates/           # Templates HTML
├── requirements.txt     # Dépendances Python
├── Procfile            # Configuration Render
└── README.md           # Ce fichier
```

## 🔧 Configuration

### Modèles disponibles
- **Vehicule** : Voitures et véhicules
- **Moto** : Motos et scooters
- **Client** : Base de données clients
- **Proprietaire** : Propriétaires des véhicules
- **Marque** : Marques de véhicules

### Fonctionnalités d'export
- Export Excel des données
- Export PDF des rapports
- Export sélectif par éléments

## 👥 Utilisation

### Interface d'administration
1. Se connecter à `/admin/`
2. Utiliser les identifiants du superutilisateur
3. Naviguer dans les différentes sections

### Gestion des véhicules
- Ajouter un nouveau véhicule
- Modifier les informations existantes
- Exporter les données
- Consulter l'historique des modifications

## 🐛 Dépannage

### Problèmes courants
- **Erreur de migration** : `python manage.py migrate --run-syncdb`
- **Fichiers statiques** : `python manage.py collectstatic`
- **Base de données** : Vérifier les permissions du fichier SQLite

### Logs
- Vérifier les logs Django : `python manage.py runserver --verbosity=2`
- Logs Render : Dashboard Render > Logs

## 📝 Licence

Ce projet est sous licence MIT.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche feature
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📞 Support

Pour toute question ou problème :
- Vérifier la documentation Django
- Consulter les logs d'erreur
- Ouvrir une issue sur GitHub

---

**Développé avec ❤️ en Django** 