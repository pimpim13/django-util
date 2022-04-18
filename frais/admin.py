from django.contrib import admin

from frais.models import ursaffModel, Bareme


@admin.register(ursaffModel)
class ursaffModel(admin.ModelAdmin):

    list_display = ('annee', 'taux_cs', 'taux_cs_non_soumise')


@admin.register(Bareme)
class BaremeAdmin(admin.ModelAdmin):

    list_display = ('annee', 'localisation', 'college', 'Repas', 'Nuit_Pdj')
