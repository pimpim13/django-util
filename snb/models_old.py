from django.db import models


class Snb_ref(models.Model):
    annee = models.IntegerField(unique=True)
    snb = models.FloatField()

    class Meta:
        ordering = ('-annee',)

    def __str__(self):
        return f'{self.annee} - {self.snb}'


class Coeff(models.Model):

    NR = models.IntegerField()
    valeur = models.FloatField()

    def __str__(self):
        return f'{self.NR} -- {self.valeur}'


class TempsDeTravail(models.Model):
    duree = models.CharField(max_length=10)
    coeff = models.FloatField()

    def __str__(self):
        return f'{self.duree} -- {self.coeff}'


class Echelon(models.Model):
    echelon = models.IntegerField()
    coeff = models.FloatField()

    def __int__(self):
        return f'Echelon {self.echelon} -- {self.coeff}'


class Inflation(models.Model):
    annee = models.IntegerField(unique=True)
    valeur = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'Année : {self.annee} - {self.valeur}'


