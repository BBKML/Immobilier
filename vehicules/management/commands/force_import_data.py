from django.core.management.base import BaseCommand
from vehicules.models import Proprietaire, Marque, Vehicule, Client, TypeVehicule, Moto
from datetime import datetime


class Command(BaseCommand):
    help = 'Force l\'import des données de test directement dans la base'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Import forcé des données de test...")
        
        try:
            # Création des données de base
            client, _ = Client.objects.get_or_create(
                nom="Client Test", 
                defaults={"contact": "0102030405", "adresse": "Abidjan"}
            )
            
            type_vehicule, _ = TypeVehicule.objects.get_or_create(nom="Type Test")
            
            # Données des véhicules
            vehicules_data = [
                {"proprietaire": "ALIBABA COTE D'IVOIRE", "marque": "DAF", "chassis": "XLRT47M50E932416", "immatriculation": "AA-278-NI", "date": "2025-01-07", "chrono": "KGOZ5ZC460", "type_tech": "TE47MS"},
                {"proprietaire": "ALIBABA COTE D'IVOIRE", "marque": "LAMBERT", "chassis": "VM3LV53EX1R09787", "immatriculation": "AA-498-NK", "date": "2025-01-07", "chrono": "KGOZ4ZC598", "type_tech": "LVF53E"},
                {"proprietaire": "TRAORE MOHAMED", "marque": "DAF", "chassis": "XLRTGH430G162879", "immatriculation": "AA-558-NN", "date": "2025-01-10", "chrono": "KGOZ5ZC885", "type_tech": "TEH430"},
                {"proprietaire": "TRAORE MOHAMED", "marque": "LECITRAILER", "chassis": "VVS1R35EASFLA1479", "immatriculation": "AA-119-NP", "date": "2025-01-10", "chrono": "KGOZ5ZC887", "type_tech": "P3AA2X"},
                {"proprietaire": "TRAORE KARIM", "marque": "LECITRAILER", "chassis": "VVS1R35EASFLF7631", "immatriculation": "AA-623-NR", "date": "2025-01-15", "chrono": "KGOZ5ZC134", "type_tech": "SR3"},
            ]
            
            # Création des véhicules
            for entry in vehicules_data:
                prop, _ = Proprietaire.objects.get_or_create(nom=entry["proprietaire"])
                marque, _ = Marque.objects.get_or_create(nom=entry["marque"])
                
                vehicule, created = Vehicule.objects.get_or_create(
                    chassis=entry["chassis"],
                    defaults={
                        "proprietaire": prop,
                        "marque": marque,
                        "client": client,
                        "type_vehicule": type_vehicule,
                        "immatriculation": entry["immatriculation"],
                        "date": entry["date"],
                        "chrono": entry["chrono"],
                        "type_tech": entry["type_tech"]
                    }
                )
                if created:
                    self.stdout.write(f"✅ Véhicule créé: {entry['immatriculation']}")
            
            # Données des motos
            motos_data = [
                {"proprietaire": "DIALLO IDI", "marque": "KIA", "chassis": "KNAJP4334H700014", "immatriculation": "AA-179-PA", "date": "2025-01-23", "chrono": "KGOZ5ZC502", "type_tech": "F2AD1D"},
                {"proprietaire": "SEKONGO NABATIN", "marque": "LECINENA", "chassis": "XL9SP3A6DM1068683", "immatriculation": "AA-709-NI", "date": "2025-01-23", "chrono": "KGOZ5ZC501", "type_tech": "SP3M98"},
            ]
            
            # Création des motos
            for entry in motos_data:
                prop, _ = Proprietaire.objects.get_or_create(nom=entry["proprietaire"])
                marque, _ = Marque.objects.get_or_create(nom=entry["marque"])
                
                moto, created = Moto.objects.get_or_create(
                    chassis=entry["chassis"],
                    defaults={
                        "proprietaire": prop,
                        "marque": marque,
                        "client": client,
                        "type_vehicule": type_vehicule,
                        "immatriculation": entry["immatriculation"],
                        "date": entry["date"],
                        "chrono": entry["chrono"],
                        "type_tech": entry["type_tech"]
                    }
                )
                if created:
                    self.stdout.write(f"✅ Moto créée: {entry['immatriculation']}")
            
            # Statistiques finales
            self.stdout.write(
                self.style.SUCCESS(
                    f"\n🎉 Import terminé avec succès!\n"
                    f"📊 Statistiques:\n"
                    f"   - Véhicules: {Vehicule.objects.count()}\n"
                    f"   - Motos: {Moto.objects.count()}\n"
                    f"   - Clients: {Client.objects.count()}\n"
                    f"   - Propriétaires: {Proprietaire.objects.count()}\n"
                    f"   - Marques: {Marque.objects.count()}\n"
                    f"\n🔗 Accédez à votre admin: https://immobilier-khoa.onrender.com/admin/"
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Erreur lors de l'import: {e}")
            ) 