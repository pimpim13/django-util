from django.db import models


class ursaff(models.Model):
    annee = models.IntegerField(max_length=4)
    taux_cs = models.DecimalField(max_digits=4, decimal_places=2)
    taux_cs_non_soumise = models.DecimalField(max_digits=4, decimal_places=2)

    