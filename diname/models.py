from django.db import models


class Famille(models.Model):
    situation = models.CharField(max_length=50)
    surface = models.IntegerField()


class Attractivite(models.Model):
    code = models.CharField(max_length=2)
    lbl_MGES = models.CharField(max_length=50, blank=True)
    mois = models.IntegerField()
    couleur = models.CharField(max_length=25, blank=True)

    def __str__(self):
        return self.code

    class Meta:
        ordering = ('code',)


class Site(models.Model):
    localisation = models.CharField(max_length=128)
    loyer = models.FloatField()

    attractivite = models.ForeignKey(Attractivite, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.localisation


class Emplois(models.Model):
    etablissement = models.CharField(max_length=50)
    libelle_emploi = models.CharField(max_length=128)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.etablissement} - {self.libelle_emploi}'
 