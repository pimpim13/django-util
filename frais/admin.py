from django.contrib import admin

from frais.models import ursaffModel, Bareme

admin.site.register(ursaffModel)


@admin.register(Bareme)
class BaremeAdmin(admin.ModelAdmin):

    list_display = ('annee', 'localisation', 'college', 'Repas', 'Nuit_Pdj')
