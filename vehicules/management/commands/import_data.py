from django.core.management.base import BaseCommand
from django.core.management import call_command
import os
import json


class Command(BaseCommand):
    help = 'Importe les données de sauvegarde dans la base de données'

    def handle(self, *args, **options):
        backup_file = 'data_backup.json'
        
        self.stdout.write(f"🔍 Recherche du fichier de sauvegarde: {backup_file}")
        
        if not os.path.exists(backup_file):
            self.stdout.write(
                self.style.ERROR(f'❌ Fichier de sauvegarde "{backup_file}" non trouvé!')
            )
            # Lister les fichiers dans le répertoire
            files = os.listdir('.')
            self.stdout.write(f"📁 Fichiers disponibles: {files}")
            return
        
        # Vérifier le contenu du fichier
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.stdout.write(f"✅ Fichier trouvé avec {len(data)} objets")
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erreur lecture fichier: {e}')
            )
            return
        
        try:
            # Importer les données
            self.stdout.write("🔄 Import des données en cours...")
            call_command('loaddata', backup_file, verbosity=1)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Données importées avec succès depuis "{backup_file}"!\n'
                    f'📊 Tous vos véhicules, clients et données sont maintenant disponibles.'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erreur lors de l\'import: {e}')
            )
            # Essayer d'importer avec plus de verbosité
            try:
                self.stdout.write("🔄 Nouvelle tentative avec plus de détails...")
                call_command('loaddata', backup_file, verbosity=2)
            except Exception as e2:
                self.stdout.write(
                    self.style.ERROR(f'❌ Échec de la deuxième tentative: {e2}')
                ) 