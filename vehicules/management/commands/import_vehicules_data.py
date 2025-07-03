from django.core.management.base import BaseCommand
from django.core.management import call_command
import os


class Command(BaseCommand):
    help = 'Importe les données des véhicules depuis le fichier JSON'

    def handle(self, *args, **options):
        backup_file = 'vehicules_data.json'
        
        self.stdout.write(f"🔍 Recherche du fichier: {backup_file}")
        
        if not os.path.exists(backup_file):
            self.stdout.write(
                self.style.ERROR(f'❌ Fichier "{backup_file}" non trouvé!')
            )
            return
        
        try:
            # Importer les données
            self.stdout.write("🔄 Import des données des véhicules...")
            call_command('loaddata', backup_file, verbosity=1)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Données des véhicules importées avec succès!\n'
                    f'📊 Tous vos véhicules, clients et données sont maintenant disponibles.'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erreur lors de l\'import: {e}')
            ) 