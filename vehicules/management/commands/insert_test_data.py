from django.core.management.base import BaseCommand
from vehicules.models import Proprietaire, Marque, Vehicule, Client, TypeVehicule
from datetime import datetime

class Command(BaseCommand):
    help = "Insère 10 véhicules de test"

    def handle(self, *args, **kwargs):
        # Création d'un client de test unique
        client, _ = Client.objects.get_or_create(nom="Client Test", defaults={"contact": "0102030405", "adresse": "Abidjan"})
        # Création d'un type de véhicule de test unique
        type_vehicule, _ = TypeVehicule.objects.get_or_create(nom="Type Test")
        data = [
            {"proprietaire": "ALIBABA COTE D'IVOIRE", "marque": "DAF", "chassis": "XLRT47M50E932416", "immatriculation": "AA-278-NI", "date": "2025-01-07", "chrono": "KGOZ5ZC460", "type_tech": "TE47MS"},
            {"proprietaire": "ALIBABA COTE D'IVOIRE", "marque": "LAMBERT", "chassis": "VM3LV53EX1R09787", "immatriculation": "AA-498-NK", "date": "2025-01-07", "chrono": "KGOZ4ZC598", "type_tech": "LVF53E"},
            {"proprietaire": "TRAORE MOHAMED", "marque": "DAF", "chassis": "XLRTGH430G162879", "immatriculation": "AA-558-NN", "date": "2025-01-10", "chrono": "KGOZ5ZC885", "type_tech": "TEH430"},
            {"proprietaire": "TRAORE MOHAMED", "marque": "LECITRAILER", "chassis": "VVS1R35EASFLA1479", "immatriculation": "AA-119-NP", "date": "2025-01-10", "chrono": "KGOZ5ZC887", "type_tech": "P3AA2X"},
            {"proprietaire": "TRAORE KARIM", "marque": "LECITRAILER", "chassis": "VVS1R35EASFLF7631", "immatriculation": "AA-623-NR", "date": "2025-01-15", "chrono": "KGOZ5ZC134", "type_tech": "SR3"},
            {"proprietaire": "CHERIF BEMA", "marque": "DAF", "chassis": "XLRT47M50E980154", "immatriculation": "AA-134-NR", "date": "2025-01-17", "chrono": "KGOZ5ZC105", "type_tech": "TE47MS"},
            {"proprietaire": "CHERIF BEMA", "marque": "FRUEHAUF", "chassis": "VKFTK34SC7R0628", "immatriculation": "AA-461-NR", "date": "2025-01-17", "chrono": "KGOZ5ZC107", "type_tech": "TX34C5"},
            {"proprietaire": "SOCIETE KONATE ET FRERES", "marque": "MERCEDES", "chassis": "WDB9340311B17509", "immatriculation": "AA-164-NR", "date": "2025-01-20", "chrono": "KGOZ5ZC109", "type_tech": "934032"},
            {"proprietaire": "SEKONGO NABATIN KASSOUM", "marque": "LECINENA", "chassis": "XL9SP3A6DM1068683", "immatriculation": "AA-709-NI", "date": "2025-01-23", "chrono": "KGOZ5ZC501", "type_tech": "SP3M98"},
            {"proprietaire": "DIALLO IDI", "marque": "KIA", "chassis": "KNAJP4334H700014", "immatriculation": "AA-179-PA", "date": "2025-01-23", "chrono": "KGOZ5ZC502", "type_tech": "F2AD1D"},
        ]
        for entry in data:
            prop, _ = Proprietaire.objects.get_or_create(nom=entry["proprietaire"])
            marque, _ = Marque.objects.get_or_create(nom=entry["marque"])
            Vehicule.objects.create(
                proprietaire=prop,
                marque=marque,
                client=client,
                type_vehicule=type_vehicule,
                chassis=entry["chassis"],
                immatriculation=entry["immatriculation"],
                date=entry["date"],
                chrono=entry["chrono"],
                type_tech=entry["type_tech"]
            )
        self.stdout.write(self.style.SUCCESS("10 véhicules de test insérés !")) 