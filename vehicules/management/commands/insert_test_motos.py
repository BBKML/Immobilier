from django.core.management.base import BaseCommand
from vehicules.models import Proprietaire, Marque, Moto, Client, TypeMoto
from datetime import datetime

class Command(BaseCommand):
    help = "Insère 10 motos de test"

    def handle(self, *args, **kwargs):
        # Création d'un client de test unique
        client, _ = Client.objects.get_or_create(nom="Client Test Moto", defaults={"contact": "0102030406", "adresse": "Abidjan"})
        # Création d'un type de moto de test unique
        type_moto, _ = TypeMoto.objects.get_or_create(nom="Type Moto Test")
        data = [
            {"proprietaire": "SANOGO MAMADOU", "marque": "SANYA", "type": "SY125-16", "chassis": "LK1PCJLGA31030043", "immatriculation": "9109FG03", "date": "2010-07-06", "no_fiche": "240/233", "societe": "PART."},
            {"proprietaire": "FONDIO BAMOUSSA", "marque": "APSONIC", "type": "AP125-9", "chassis": "LAAA...2900943", "immatriculation": "9917FG03", "date": "2010-09-15", "no_fiche": "1625/1617", "societe": "PART. ok"},
            {"proprietaire": "SILUE SINANGON AMINATA", "marque": "KTM", "type": "X1", "chassis": "LP5XCHLC6A0181094", "immatriculation": "2799FG03", "date": "2010-10-05", "no_fiche": "2269/2262", "societe": "COIC OK"},
            {"proprietaire": "COULIBALY SARAN", "marque": "KTM", "type": "X1", "chassis": "LP5XCHLC9X0106815", "immatriculation": "2791FG03", "date": "2010-10-05", "no_fiche": "2268/2254", "societe": "COIC"},
            {"proprietaire": "KONE EPSE DIOMANDE SITA", "marque": "HAOJUE", "type": "110-2", "chassis": "LC6XCHX1580804322", "immatriculation": "9101FG03", "date": "2010-10-05", "no_fiche": "2271/2260", "societe": "COIC OK"},
            {"proprietaire": "COULIBALY SALIMATA", "marque": "KTM", "type": "X1", "chassis": "LPXCHLC6A0157314", "immatriculation": "2798FG03", "date": "2010-10-05", "no_fiche": "2270/2258", "societe": "COIC OK"},
            {"proprietaire": "ASSERY GNAGNE VIVIEN", "marque": "ACCES", "type": "AC101", "chassis": "LHJXCHLA79M100370", "immatriculation": "8243FG03", "date": "2010-10-20", "no_fiche": "3065/3088", "societe": "PART.OK"},
            {"proprietaire": "FOFANA MOUSSA SALIA", "marque": "SANYA", "type": "SY125-8", "chassis": "LK1PCJLB891116213", "immatriculation": "8548FG03", "date": "2010-11-09", "no_fiche": "3472/3459", "societe": "COIC"},
            {"proprietaire": "SANOGO DRISSA", "marque": "SANYA", "type": "SY125-16", "chassis": "LK1PCJLG881022952", "immatriculation": "8585FG03", "date": "2010-11-08", "no_fiche": "3434/3421", "societe": "COIC"},
            {"proprietaire": "DIAGONE BI GOHI JANVIER", "marque": "SANYA", "type": "SY125-8", "chassis": "LK1PCJLB891116474", "immatriculation": "8585FG03", "date": "2010-11-08", "no_fiche": "3432/3418", "societe": "COIC"},
        ]
        inserted = 0
        for entry in data:
            if Moto.objects.filter(immatriculation=entry["immatriculation"]).exists():
                continue
            prop, _ = Proprietaire.objects.get_or_create(nom=entry["proprietaire"])
            marque, _ = Marque.objects.get_or_create(nom=entry["marque"])
            type_moto_obj, _ = TypeMoto.objects.get_or_create(nom=entry["type"])
            Moto.objects.create(
                proprietaire=prop,
                marque=marque,
                client=client,
                type_moto=type_moto_obj,
                chassis=entry["chassis"],
                immatriculation=entry["immatriculation"],
                date=entry["date"],
                no_fiche=entry["no_fiche"],
                couleur=entry["societe"]
            )
            inserted += 1
        self.stdout.write(self.style.SUCCESS(f"{inserted} motos de test insérées !")) 