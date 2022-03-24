from django.db import models
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator

annee_en_cours = date.today().year
annee_min = 2021


class ursaffModel(models.Model):
    annee = models.IntegerField()
    taux_cs = models.DecimalField(max_digits=4, decimal_places=2)
    taux_cs_non_soumise = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return str(self.annee)


class Bareme(models.Model):
    annee = models.IntegerField()
    localisation = models.CharField(max_length=200)
    college = models.CharField(max_length=20)
    Repas = models.DecimalField(max_digits=5, decimal_places=2)
    Nuit_Pdj = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.annee} - {self.localisation}"

