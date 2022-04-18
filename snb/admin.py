from django.contrib import admin
from snb.models import Snb_ref, Coeff, TempsDeTravail, Inflation, Echelon


@admin.register(Coeff)
class Coeff(admin.ModelAdmin):
    list_display = ('NR', 'valeur')


@admin.register(Snb_ref)
class Snb_ref(admin.ModelAdmin):
    list_display = ('annee', 'snb')


@admin.register(TempsDeTravail)
class TempsDeTravail(admin.ModelAdmin):
    list_display = ('duree', 'coeff')


@admin.register(Inflation)
class Inflation(admin.ModelAdmin):
    list_display = ('annee', 'valeur')


@admin.register(Echelon)
class Echelon(admin.ModelAdmin):
    list_display = ('echelon', 'coeff')