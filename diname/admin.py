from django.contrib import admin

from diname.models import Famille, Site, Attractivite, Emplois


@admin.register(Famille)
class Famille(admin.ModelAdmin):
    list_display = ('situation', 'surface')


@admin.register(Attractivite)
class Attractivite(admin.ModelAdmin):
    list_display = ('code', 'lbl_MGES', 'mois', 'couleur')


@admin.register(Site)
class Site(admin.ModelAdmin):
    list_display = ('localisation', 'loyer', 'attractivite',)


@admin.register(Emplois)
class Emplois(admin.ModelAdmin):
    list_display = ('etablissement', 'libelle_emploi', 'actif',)
