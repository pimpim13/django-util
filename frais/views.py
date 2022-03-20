from pprint import pprint

from django.shortcuts import render, redirect
from .forms import FraisForm
from frais import parse_xl


def frais(request):
    bareme_total = parse_xl.get_json('static/datas/2022.json')
    taux_ursaff = parse_xl.get_json('static/datas/ursaff.json')

    taux_cs_ecart = taux_ursaff['2022']['taux_cs_ecart']/100
    taux_cs_non_soumises = taux_ursaff['2022']['taux_cs_non_soumises']/100
    # print(taux_cs_non_soumises, taux_cs_ecart)

    valeurs = {}
    nuit, repas, acoss_r, acoss_n = 0.0, 0.0, 0.0, 0.0
    retenue_ecart_r = 0.0
    retenue_ecart_n = 0.0
    retenue_cs_non_soumises_r = 0.0
    retenue_cs_non_soumises_n = 0.0

    if request.method == 'GET':
        localisation = request.GET.get('localisation', '')
        taux = float(request.GET.get('taux', 0))
        college = request.GET.get('college', '')

        valeurs = request.GET
        if localisation and college:
            nuit = bareme_total[localisation][college]['N+PD']
            repas = bareme_total[localisation][college]['R']
            acoss_r = bareme_total[localisation]['ACOSS']['R']
            acoss_n = bareme_total[localisation]['ACOSS']['N+PD']

            retenue_ecart_r = round((repas - acoss_r) * taux_cs_ecart, 2)
            retenue_ecart_n = round((nuit - acoss_n) * taux_cs_ecart, 2)

            retenue_cs_non_soumises_r = round((repas-acoss_r) * (1 - taux_cs_non_soumises) * 0.9 * taux/100, 2)
            retenue_cs_non_soumises_n = round((nuit-acoss_n) * (1 - taux_cs_non_soumises) * 0.9 * taux/100,2)

    form = FraisForm(valeurs) if valeurs else FraisForm()
    context = {'form': form,
               'nuit': nuit,
               'repas': repas,
               'acoss_r': acoss_r,
               'acoss_n': acoss_n,
               'retenue_ecart_r': retenue_ecart_r,
               'retenue_ecart_n': retenue_ecart_n,
               'retenue_cs_non_soumises_r': retenue_cs_non_soumises_r,
               'retenue_cs_non_soumises_n': retenue_cs_non_soumises_n,
               }
    # pprint(context)

    return render(request, 'frais/frais.html', context)


def maj_ursaff(request):
    context = {}
    taux_ursaff = parse_xl.get_json('static/datas/ursaff.json')
    # taux_cs_ecart = taux_ursaff['2022']['taux_cs_ecart']/100
    # taux_cs_non_soumises = taux_ursaff['2022']['taux_cs_non_soumises']/100

    context['ursaff'] = taux_ursaff


    return render(request, 'frais/ursaff.html', context=context)
