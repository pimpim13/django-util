# Generated by Django 4.0.3 on 2022-03-21 07:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ursaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annee', models.IntegerField(default=2022, validators=[django.core.validators.MinValueValidator(2021), django.core.validators.MaxValueValidator(2022)])),
                ('taux_cs', models.DecimalField(decimal_places=2, max_digits=4)),
                ('taux_cs_non_soumise', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
    ]
