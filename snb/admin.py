from django.contrib import admin
from snb.models import Snb_ref, TempsDeTravail, Inflation, Echelon, Coeff_New, Snb_ref_New


@admin.register(Coeff_New)
class Coeff(admin.ModelAdmin):
    list_display = ('date_application', 'NR', 'valeur')


@admin.register(Snb_ref)
class Snb_ref(admin.ModelAdmin):
    list_display = ('annee', 'snb')


@admin.register(Snb_ref_New)
class Snb_ref(admin.ModelAdmin):
    list_display = ('annee', 'snb', 'date_application')

@admin.register(TempsDeTravail)
class TempsDeTravail(admin.ModelAdmin):
    list_display = ('duree', 'coeff')


@admin.register(Inflation)
class Inflation(admin.ModelAdmin):
    list_display = ('annee', 'valeur')


@admin.register(Echelon)
class Echelon(admin.ModelAdmin):
    list_display = ('echelon', 'coeff')