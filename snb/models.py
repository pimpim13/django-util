from django.db import models


class Snb_ref(models.Model):
    annee = models.IntegerField(unique=True)
    snb = models.FloatField()

    class Meta:
        ordering = ('-annee',)

    def __str__(self):
        return f'{self.annee} - {self.snb}'


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


class Coeff_New(models.Model):
    NR = models.IntegerField()
    valeur = models.FloatField()
    date_application = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ('-date_application', 'NR')

    def __str__(self):
        return f'{self.date_application} -- {self.NR} -- {self.valeur}'


class Snb_ref_New(models.Model):
    annee = models.IntegerField()
    snb = models.FloatField()
    date_application = models.DateField(blank=True, null=True, unique=True)

    class Meta:
        ordering = ('-annee', '-date_application')

    def __str__(self):
        return f'{self.date_application} - {self.snb}'
