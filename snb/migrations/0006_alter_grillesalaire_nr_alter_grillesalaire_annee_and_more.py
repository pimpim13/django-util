# Generated by Django 4.0.3 on 2022-04-13 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snb', '0005_alter_grillesalaire_ech1_alter_grillesalaire_ech10_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grillesalaire',
            name='NR',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='grillesalaire',
            name='annee',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='grillesalaire',
            name='maj_res',
            field=models.FloatField(null=True),
        ),
    ]