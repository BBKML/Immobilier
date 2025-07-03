from django.db import models
from simple_history.models import HistoricalRecords
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re

class Client(models.Model):
    nom = models.CharField(max_length=255)
    contact = models.CharField(max_length=100, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['nom']

    def __str__(self):
        return self.nom

    def clean(self):
        if not self.nom or self.nom.strip() == '':
            raise ValidationError({'nom': 'Le nom du client est obligatoire'})

class Proprietaire(models.Model):
    nom = models.CharField(max_length=255)
    contact = models.CharField(max_length=100, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Propriétaire"
        verbose_name_plural = "Propriétaires"
        ordering = ['nom']

    def __str__(self):
        return self.nom

    def clean(self):
        if not self.nom or self.nom.strip() == '':
            raise ValidationError({'nom': 'Le nom du propriétaire est obligatoire'})

class CategorieVehicule(models.Model):
    nom = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Catégorie de véhicule"
        verbose_name_plural = "Catégories de véhicules"
        ordering = ['nom']

    def __str__(self):
        return self.nom

class Marque(models.Model):
    nom = models.CharField(max_length=100)
    categorie = models.ForeignKey(CategorieVehicule, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Marque"
        verbose_name_plural = "Marques"
        ordering = ['nom']
        unique_together = ['nom', 'categorie']

    def __str__(self):
        return f"{self.nom} ({self.categorie})"

    def clean(self):
        if not self.nom or self.nom.strip() == '':
            raise ValidationError({'nom': 'Le nom de la marque est obligatoire'})

class TypeVehicule(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Type de véhicule"
        verbose_name_plural = "Types de véhicules"
        ordering = ['nom']

    def __str__(self):
        return self.nom

    def clean(self):
        if not self.nom or self.nom.strip() == '':
            raise ValidationError({'nom': 'Le nom du type de véhicule est obligatoire'})

class TypeMoto(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Type de moto"
        verbose_name_plural = "Types de motos"
        ordering = ['nom']

    def __str__(self):
        return self.nom

    def clean(self):
        if not self.nom or self.nom.strip() == '':
            raise ValidationError({'nom': 'Le nom du type de moto est obligatoire'})

class Vehicule(models.Model):
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
        ('en_maintenance', 'En maintenance'),
    ]
    
    # Données du véhicule (obligatoires)
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE)
    type_vehicule = models.ForeignKey(TypeVehicule, on_delete=models.CASCADE)
    chassis = models.CharField(max_length=100, unique=True)
    immatriculation = models.CharField(
        max_length=50, 
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Z]{2}-\d{3,4}-[A-Z]{2}$',
                message="Format d'immatriculation invalide (ex: AA-123-AB)"
            )
        ]
    )
    
    # Données administratives (optionnelles)
    date = models.DateField(blank=True, null=True)
    chrono = models.CharField(max_length=100, blank=True, null=True)
    type_tech = models.CharField(max_length=100, blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='actif')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    proprietaire = models.ForeignKey(Proprietaire, on_delete=models.CASCADE, blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Véhicule"
        verbose_name_plural = "Véhicules"
        ordering = ['-date', 'immatriculation']

    def __str__(self):
        return f"{self.immatriculation} - {self.marque.nom}"

    def clean(self):
        super().clean()
        if not self.chassis or self.chassis.strip() == '':
            raise ValidationError({'chassis': 'Le numéro de châssis est obligatoire'})
        
        # Validation du format d'immatriculation
        if not re.match(r'^[A-Z]{2}-\d{3,4}-[A-Z]{2}$', self.immatriculation):
            raise ValidationError({'immatriculation': "Format d'immatriculation invalide (ex: AA-123-AB)"})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Moto(models.Model):
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
        ('en_maintenance', 'En maintenance'),
    ]
    
    # Données de la moto (obligatoires)
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE)
    type_moto = models.ForeignKey(TypeMoto, on_delete=models.CASCADE)
    chassis = models.CharField(max_length=100, unique=True)
    immatriculation = models.CharField(
        max_length=50, 
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{4}[A-Z]{2}\d{2}$',
                message="Format d'immatriculation invalide (ex: 1234FG03)"
            )
        ]
    )
    
    # Données administratives (optionnelles)
    date = models.DateField(blank=True, null=True)
    no_fiche = models.CharField(max_length=100, blank=True, null=True)
    couleur = models.CharField(max_length=50, blank=True, null=True)
    couleurs = models.CharField(max_length=255, blank=True, null=True, help_text="Liste des couleurs séparées par une virgule")
    cellulaire = models.CharField(max_length=50, blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='actif')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    proprietaire = models.ForeignKey(Proprietaire, on_delete=models.CASCADE, blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Moto"
        verbose_name_plural = "Motos"
        ordering = ['-date', 'immatriculation']

    def __str__(self):
        return f"{self.immatriculation} - {self.marque.nom}"

    def clean(self):
        super().clean()
        if not self.chassis or self.chassis.strip() == '':
            raise ValidationError({'chassis': 'Le numéro de châssis est obligatoire'})
        
        # Validation du format d'immatriculation
        if not re.match(r'^\d{4}[A-Z]{2}\d{2}$', self.immatriculation):
            raise ValidationError({'immatriculation': "Format d'immatriculation invalide (ex: 1234FG03)"})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)