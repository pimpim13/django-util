# Generated by Django 4.0.3 on 2022-04-13 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snb', '0003_grillesalaire_nr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grillesalaire',
            name='coeff',
            field=models.FloatField(null=True),
        ),
    ]
