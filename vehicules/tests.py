from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Client, Proprietaire, Marque, TypeVehicule, TypeMoto, Vehicule, Moto

class ClientModelTest(TestCase):
    def test_client_creation(self):
        client = Client.objects.create(
            nom="Test Client",
            contact="0123456789",
            adresse="Test Address"
        )
        self.assertEqual(client.nom, "Test Client")
        self.assertEqual(str(client), "Test Client")

    def test_client_validation(self):
        with self.assertRaises(ValidationError):
            client = Client(nom="")
            client.full_clean()

class ProprietaireModelTest(TestCase):
    def test_proprietaire_creation(self):
        proprietaire = Proprietaire.objects.create(
            nom="Test Propriétaire",
            contact="0123456789",
            adresse="Test Address"
        )
        self.assertEqual(proprietaire.nom, "Test Propriétaire")
        self.assertEqual(str(proprietaire), "Test Propriétaire")

    def test_proprietaire_validation(self):
        with self.assertRaises(ValidationError):
            proprietaire = Proprietaire(nom="")
            proprietaire.full_clean()

class MarqueModelTest(TestCase):
    def test_marque_creation(self):
        marque = Marque.objects.create(
            nom="Test Marque",
            categorie="voiture"
        )
        self.assertEqual(marque.nom, "Test Marque")
        self.assertEqual(str(marque), "Test Marque (voiture)")

    def test_marque_validation(self):
        with self.assertRaises(ValidationError):
            marque = Marque(nom="")
            marque.full_clean()

class VehiculeModelTest(TestCase):
    def setUp(self):
        self.marque = Marque.objects.create(nom="Test Marque", categorie="voiture")
        self.type_vehicule = TypeVehicule.objects.create(nom="Test Type")
        self.client = Client.objects.create(nom="Test Client")
        self.proprietaire = Proprietaire.objects.create(nom="Test Propriétaire")

    def test_vehicule_creation(self):
        vehicule = Vehicule.objects.create(
            marque=self.marque,
            type_vehicule=self.type_vehicule,
            chassis="TEST123456789",
            immatriculation="AA-123-AB",
            client=self.client,
            proprietaire=self.proprietaire
        )
        self.assertEqual(vehicule.immatriculation, "AA-123-AB")
        self.assertEqual(str(vehicule), "AA-123-AB - Test Marque")

    def test_vehicule_immatriculation_validation(self):
        with self.assertRaises(ValidationError):
            vehicule = Vehicule(
                marque=self.marque,
                type_vehicule=self.type_vehicule,
                chassis="TEST123456789",
                immatriculation="INVALID-FORMAT"
            )
            vehicule.full_clean()

    def test_vehicule_chassis_validation(self):
        with self.assertRaises(ValidationError):
            vehicule = Vehicule(
                marque=self.marque,
                type_vehicule=self.type_vehicule,
                chassis="",
                immatriculation="AA-123-AB"
            )
            vehicule.full_clean()

class MotoModelTest(TestCase):
    def setUp(self):
        self.marque = Marque.objects.create(nom="Test Marque", categorie="moto")
        self.type_moto = TypeMoto.objects.create(nom="Test Type")
        self.client = Client.objects.create(nom="Test Client")
        self.proprietaire = Proprietaire.objects.create(nom="Test Propriétaire")

    def test_moto_creation(self):
        moto = Moto.objects.create(
            marque=self.marque,
            type_moto=self.type_moto,
            chassis="TEST123456789",
            immatriculation="1234FG03",
            client=self.client,
            proprietaire=self.proprietaire
        )
        self.assertEqual(moto.immatriculation, "1234FG03")
        self.assertEqual(str(moto), "1234FG03 - Test Marque")

    def test_moto_immatriculation_validation(self):
        with self.assertRaises(ValidationError):
            moto = Moto(
                marque=self.marque,
                type_moto=self.type_moto,
                chassis="TEST123456789",
                immatriculation="INVALID-FORMAT"
            )
            moto.full_clean()

    def test_moto_chassis_validation(self):
        with self.assertRaises(ValidationError):
            moto = Moto(
                marque=self.marque,
                type_moto=self.type_moto,
                chassis="",
                immatriculation="1234FG03"
            )
            moto.full_clean()

class AdminActionsTest(TestCase):
    def setUp(self):
        self.marque = Marque.objects.create(nom="Test Marque", categorie="voiture")
        self.type_vehicule = TypeVehicule.objects.create(nom="Test Type")
        self.client = Client.objects.create(nom="Test Client")
        self.proprietaire = Proprietaire.objects.create(nom="Test Propriétaire")
        
        self.vehicule = Vehicule.objects.create(
            marque=self.marque,
            type_vehicule=self.type_vehicule,
            chassis="TEST123456789",
            immatriculation="AA-123-AB",
            client=self.client,
            proprietaire=self.proprietaire,
            statut="actif"
        )

    def test_marquer_actif_action(self):
        from vehicules.admin import marquer_actif
        self.vehicule.statut = "inactif"
        self.vehicule.save()
        
        marquer_actif(None, None, Vehicule.objects.filter(id=self.vehicule.id))
        self.vehicule.refresh_from_db()
        self.assertEqual(self.vehicule.statut, "actif")

    def test_marquer_inactif_action(self):
        from vehicules.admin import marquer_inactif
        self.vehicule.statut = "actif"
        self.vehicule.save()
        
        marquer_inactif(None, None, Vehicule.objects.filter(id=self.vehicule.id))
        self.vehicule.refresh_from_db()
        self.assertEqual(self.vehicule.statut, "inactif") 