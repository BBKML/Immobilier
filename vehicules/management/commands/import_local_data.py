from django.core.management.base import BaseCommand
from django.core.management import call_command
import os
import json


class Command(BaseCommand):
    help = 'Importe automatiquement les données locales sur Render'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Import automatique des données locales...")
        
        # Essayer différents noms de fichiers de sauvegarde
        backup_files = [
            'local_data_backup.json',
            'data_backup.json',
            'vehicules_data.json'
        ]
        
        for backup_file in backup_files:
            if os.path.exists(backup_file):
                self.stdout.write(f"🔍 Fichier trouvé: {backup_file}")
                
                try:
                    # Vérifier le contenu du fichier
                    with open(backup_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    self.stdout.write(f"✅ Fichier valide avec {len(data)} objets")
                    
                    # Importer les données
                    self.stdout.write("🔄 Import des données en cours...")
                    call_command('loaddata', backup_file, verbosity=1)
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"🎉 Import réussi depuis {backup_file}!\n"
                            f"📊 Toutes vos données locales sont maintenant sur Render!"
                        )
                    )
                    return
                    
                except json.JSONDecodeError as e:
                    self.stdout.write(
                        self.style.WARNING(f"⚠️ Fichier {backup_file} corrompu: {e}")
                    )
                    continue
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"❌ Erreur import {backup_file}: {e}")
                    )
                    continue
        
        # Si aucun fichier n'a fonctionné, utiliser les données de test
        self.stdout.write(
            self.style.WARNING("⚠️ Aucun fichier de sauvegarde valide trouvé, utilisation des données de test")
        )
        
        try:
            call_command('force_import_data')
            self.stdout.write(
                self.style.SUCCESS("✅ Données de test importées avec succès!")
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Erreur import données de test: {e}")
            ) 