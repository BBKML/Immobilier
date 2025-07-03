# Generated manually

from django.db import migrations

def populate_categories(apps, schema_editor):
    """Crée les catégories de véhicules"""
    CategorieVehicule = apps.get_model('vehicules', 'CategorieVehicule')
    
    # Créer les catégories principales
    categories = [
        'Véhicule',
        'Moto',
        'Camion',
        'Semi-remorque',
        'Remorque',
        'Tracteur routier',
        'Tracteur agricole'
    ]
    
    for nom in categories:
        categorie, created = CategorieVehicule.objects.get_or_create(nom=nom)
        if created:
            print(f"✅ Catégorie créée: {nom}")
        else:
            print(f"ℹ️ Catégorie existante: {nom}")
    
    print(f"✅ {len(categories)} catégories disponibles")

def reverse_populate_categories(apps, schema_editor):
    """Supprime les catégories créées"""
    CategorieVehicule = apps.get_model('vehicules', 'CategorieVehicule')
    CategorieVehicule.objects.all().delete()
    print("✅ Catégories supprimées")

class Migration(migrations.Migration):

    dependencies = [
        ('vehicules', '0010_categorievehicule_alter_client_options_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_categories, reverse_populate_categories),
    ] 