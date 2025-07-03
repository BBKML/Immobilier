from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import IntegrityError


class Command(BaseCommand):
    help = 'Crée un superuser par défaut pour l\'application'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin123'
        
        try:
            # Vérifier si l'utilisateur existe déjà
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'Le superuser "{username}" existe déjà.')
                )
                return
            
            # Créer le superuser
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Superuser créé avec succès!\n'
                    f'Username: {username}\n'
                    f'Email: {email}\n'
                    f'Password: {password}\n'
                    f'⚠️  IMPORTANT: Changez le mot de passe après la première connexion!'
                )
            )
            
        except IntegrityError:
            self.stdout.write(
                self.style.ERROR('Erreur lors de la création du superuser.')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erreur inattendue: {e}')
            ) 