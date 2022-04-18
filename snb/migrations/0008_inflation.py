# Generated by Django 4.0.3 on 2022-04-13 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snb', '0007_coeff_tempsdetravail_delete_grillesalaire'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inflation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annee', models.IntegerField(unique=True)),
                ('inflation', models.FloatField()),
            ],
        ),
    ]
