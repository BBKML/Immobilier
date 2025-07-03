# Generated manually

from django.db import migrations

def update_voiture_to_vehicule(apps, schema_editor):
    """Met à jour les catégories 'voiture' en 'véhicule'"""
    Marque = apps.get_model('vehicules', 'Marque')
    
    # Mettre à jour toutes les marques avec catégorie 'voiture'
    marques_voiture = Marque.objects.filter(categorie='voiture')
    marques_voiture.update(categorie='vehicule')
    
    print(f"✅ {marques_voiture.count()} marques mises à jour de 'voiture' vers 'véhicule'")

def reverse_vehicule_to_voiture(apps, schema_editor):
    """Remet à jour les catégories 'véhicule' en 'voiture' (rollback)"""
    Marque = apps.get_model('vehicules', 'Marque')
    
    # Mettre à jour toutes les marques avec catégorie 'vehicule'
    marques_vehicule = Marque.objects.filter(categorie='vehicule')
    marques_vehicule.update(categorie='voiture')
    
    print(f"✅ {marques_vehicule.count()} marques remises à jour de 'véhicule' vers 'voiture'")

class Migration(migrations.Migration):

    dependencies = [
        ('vehicules', '0006_alter_historicalmoto_date_and_more'),
    ]

    operations = [
        migrations.RunPython(update_voiture_to_vehicule, reverse_vehicule_to_voiture),
    ] 