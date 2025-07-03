from django.core.management.base import BaseCommand
from django.core.management import call_command
import os


class Command(BaseCommand):
    help = 'Importe les données de sauvegarde dans la base de données'

    def handle(self, *args, **options):
        backup_file = 'data_backup.json'
        
        if not os.path.exists(backup_file):
            self.stdout.write(
                self.style.ERROR(f'Fichier de sauvegarde "{backup_file}" non trouvé!')
            )
            return
        
        try:
            # Importer les données
            call_command('loaddata', backup_file, verbosity=0)
            
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