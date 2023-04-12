# Generated by Django 4.0.3 on 2023-03-17 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diname', '0003_attractivite_couleur'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emplois',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etablissement', models.CharField(max_length=50)),
                ('libelle_emploi', models.CharField(max_length=128)),
                ('actif', models.BooleanField(default=True)),
            ],
        ),
    ]