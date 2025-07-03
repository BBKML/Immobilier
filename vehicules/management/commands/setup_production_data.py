from django.core.management.base import BaseCommand
from django.core.management import call_command
import os


class Command(BaseCommand):
    help = 'Configure les données de production (import + fallback)'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Configuration des données de production...")
        
        # Essayer d'abord l'import des données réelles
        backup_file = 'data_backup.json'
        
        if os.path.exists(backup_file):
            self.stdout.write("📊 Tentative d'import des données réelles...")
            try:
                call_command('import_data')
                self.stdout.write(
                    self.style.SUCCESS("✅ Données réelles importées avec succès!")
                )
                return
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f"⚠️ Échec import données réelles: {e}")
                )
        
        # Fallback: utiliser les données de test
        self.stdout.write("🔄 Utilisation des données de test...")
        try:
            call_command('insert_test_data')
            call_command('insert_test_motos')
            self.stdout.write(
                self.style.SUCCESS("✅ Données de test importées avec succès!")
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Échec import données de test: {e}")
            ) 