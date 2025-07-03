from django.core.management.base import BaseCommand
from django.core.management import call_command
import os
import json


class Command(BaseCommand):
    help = 'Importe automatiquement les données locales sur Render'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Import automatique des données locales...")
        
        # Essayer différents noms de fichiers de sauvegarde (déployables en priorité)
        backup_files = [
            'deployable_final_cleaned_local_data_backup_fixed.json',
            'deployable_final_cleaned_fixed_data_backup.json',
            'deployable_final_cleaned_fixed_vehicules_data.json',
            'final_cleaned_local_data_backup_fixed.json',
            'final_cleaned_fixed_data_backup.json',
            'final_cleaned_fixed_vehicules_data.json',
            'cleaned_local_data_backup_fixed.json',
            'cleaned_fixed_data_backup.json',
            'cleaned_fixed_vehicules_data.json',
            'local_data_backup_fixed.json',
            'fixed_local_data_backup.json',
            'fixed_data_backup.json',
            'fixed_vehicules_data.json',
            'local_data_backup.json',
            'data_backup.json',
            'vehicules_data.json'
        ]
        
        for backup_file in backup_files:
            if os.path.exists(backup_file):
                self.stdout.write(f"🔍 Fichier trouvé: {backup_file}")
                
                try:
                    # Essayer différents encodages
                    encodings_to_try = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']
                    data = None
                    used_encoding = None
                    
                    for encoding in encodings_to_try:
                        try:
                            with open(backup_file, 'r', encoding=encoding) as f:
                                data = json.load(f)
                                used_encoding = encoding
                                break
                        except (UnicodeDecodeError, json.JSONDecodeError):
                            continue
                    
                    if data is None:
                        raise Exception("Impossible de décoder le fichier avec aucun encodage")
                    
                    self.stdout.write(f"✅ Fichier valide avec {len(data)} objets (encodage: {used_encoding})")
                    
                    # Créer un fichier temporaire avec encodage UTF-8
                    temp_file = f"temp_{backup_file}"
                    with open(temp_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    
                    # Importer les données
                    self.stdout.write("🔄 Import des données en cours...")
                    call_command('loaddata', temp_file, verbosity=1)
                    
                    # Nettoyer le fichier temporaire
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                    
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