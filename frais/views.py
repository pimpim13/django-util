from pprint import pprint
from django.http import HttpResponse, HttpResponseRedirect
import json

from django.shortcuts import render, redirect
from .forms import FraisForm, updateUrsaffForm, newUrsaffForm
from frais.models import ursaffModel, Bareme
from datetime import date


def frais(request):

    bareme_total = Bareme.objects.filter(annee=date.today().year)
    taux_ursaff = ursaffModel.objects.filter(annee=date.today().year)

    if bareme_total.count() == 0:
        annee_bareme = Bareme.objects.last().annee
    else:
        annee_bareme = date.today().year

    return redirect('frais_an', annee_bareme)
#     return redirect('frais_an', an=annee_bareme)


def frais_an(request, an):

    list_taux = ursaffModel.objects.get(annee=an)
    taux_cs_ecart = float(list_taux.taux_cs)/100
    taux_cs_non_soumises = float(list_taux.taux_cs_non_soumise)/100

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

            nuit = Bareme.objects.get(annee=an, localisation=localisation, college=college,).Nuit_Pdj
            repas = Bareme.objects.get(annee=an, localisation=localisation, college=college,).Repas
            acoss_r = Bareme.objects.get(annee=an, localisation=localisation, college='ACOSS',).Repas
            acoss_n = Bareme.objects.get(annee=an, localisation=localisation, college='ACOSS',).Nuit_Pdj

            retenue_ecart_r = round((repas - acoss_r) * taux_cs_ecart, 2)
            retenue_ecart_n = round((nuit - acoss_n) * taux_cs_ecart, 2)

            retenue_cs_non_soumises_r = round((repas-acoss_r) * (1 - taux_cs_non_soumises) * 0.9 * taux/100, 2)
            retenue_cs_non_soumises_n = round((nuit-acoss_n) * (1 - taux_cs_non_soumises) * 0.9 * taux/100, 2)

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
               'message': an
               }
    # pprint(context)

    return render(request, 'frais/frais.html', context)


def maj_ursaff(request):

    context = {}
    list_taux = ursaffModel.objects.all()
    context['list_taux'] = list_taux
    context['creation'] = True

    return render(request, 'frais/ursaff.html', context=context)


def maj_ursaff_item(request, item):

    context = {}
    list_taux = ursaffModel.objects.get(annee=item)
    taux_cs_ecart = list_taux.taux_cs
    taux_cs_non_soumise = list_taux.taux_cs_non_soumise
    form = updateUrsaffForm(initial={'annee': item,
                                     'taux_cs': taux_cs_ecart,
                                     'taux_cs_non_soumise': taux_cs_non_soumise,})
    context['an'] = item
    if request.method == 'POST':
        form = updateUrsaffForm(request.POST)
        if form.is_valid():
            list_taux.taux_cs = form.cleaned_data['taux_cs']
            list_taux.taux_cs_non_soumise = form.cleaned_data['taux_cs_non_soumise']
            list_taux.save()
            success = True
            return redirect('ursaff')
        else:
            success = False

        context['success'] = success
        context['form'] = form
        return render(request, 'frais/ursaff_update.html', context=context)

    context['form'] = form

    return render(request, 'frais/ursaff_update.html', context=context)


def del_ursaff_item(request, item):
    a = ursaffModel.objects.get(annee=item)
    a.delete()

    return redirect('ursaff')


def new_ursaff_item(request):

    context = {}
    form = newUrsaffForm()

    if request.method == 'POST':
        form = newUrsaffForm(request.POST)

    if form.is_valid():
        form.save()
        return redirect('ursaff')

    context['form'] = form

    return render(request, 'frais/ursaff_new.html', context=context)


def jsonTodb(file):

    with open(file,'r') as f:
        data = json.load(f)

    for element in data.keys():
        for x in data[element].keys():
            print(x)
            repas = data[element][x]['R']
            nuit = data[element][x]['N+PD']

            print(element, x, repas, nuit)


def new_bareme_item(request):
    return None