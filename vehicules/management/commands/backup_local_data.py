from django.core.management.base import BaseCommand
from django.core.management import call_command
import os
import json


class Command(BaseCommand):
    help = 'Sauvegarde automatique de toutes les données locales'

    def handle(self, *args, **options):
        self.stdout.write("🔄 Sauvegarde automatique des données locales...")
        
        try:
            # Créer un fichier de sauvegarde complet
            backup_file = 'local_data_backup.json'
            
            # Exporter toutes les données (sauf auth.permission et contenttypes)
            call_command('dumpdata', 
                        '--exclude', 'auth.permission',
                        '--exclude', 'contenttypes',
                        '--indent', '2',
                        '--output', backup_file,
                        verbosity=0)
            
            # Vérifier que le fichier a été créé
            if os.path.exists(backup_file):
                file_size = os.path.getsize(backup_file)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✅ Sauvegarde créée: {backup_file} ({file_size} bytes)\n"
                        f"📊 Toutes vos données locales sont sauvegardées!"
                    )
                )
            else:
                self.stdout.write(
                    self.style.ERROR("❌ Erreur: Fichier de sauvegarde non créé")
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Erreur lors de la sauvegarde: {e}")
            ) 