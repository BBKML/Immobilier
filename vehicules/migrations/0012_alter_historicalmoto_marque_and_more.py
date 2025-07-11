# Generated by Django 5.2.3 on 2025-07-03 13:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicules', '0011_populate_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalmoto',
            name='marque',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='vehicules.marque'),
        ),
        migrations.AlterField(
            model_name='historicalvehicule',
            name='marque',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='vehicules.marque'),
        ),
        migrations.AlterField(
            model_name='marque',
            name='categorie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicules.categorievehicule'),
        ),
        migrations.AlterField(
            model_name='moto',
            name='marque',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicules.marque'),
        ),
        migrations.AlterField(
            model_name='vehicule',
            name='marque',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicules.marque'),
        ),
    ]
