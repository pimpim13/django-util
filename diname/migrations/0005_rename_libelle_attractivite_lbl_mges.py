# Generated by Django 4.0.3 on 2023-03-20 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diname', '0004_emplois'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attractivite',
            old_name='libelle',
            new_name='lbl_MGES',
        ),
    ]