
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import json

from django.shortcuts import render, redirect
from .forms import FraisForm, updateUrsaffForm, newUrsaffForm
from frais.models import ursaffModel, Bareme
from datetime import date
from frais import parse_xl


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
               'message': an,
               }
    # pprint(context)

    return render(request, 'frais/frais.html', context)


@login_required
def maj_ursaff(request):

    if not request.user.is_staff:
        messages.error(request, "Vous n'avez pas les droits suffisants pour accéder à cette page")
        return redirect('frais')

    context = {}
    list_taux = ursaffModel.objects.all()
    context['list_taux'] = list_taux
    context['new'] = False

    return render(request, 'frais/ursaff.html', context=context)


@login_required
def maj_ursaff_item(request, item):

    if not request.user.is_staff:
        messages.error(request, "Vous n'avez pas les droits suffisants pour accéder à cette page")
        return redirect('frais')

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
        context['new'] = False
        return render(request, 'frais/ursaff_update.html', context=context)

    context['form'] = form

    return render(request, 'frais/ursaff_update.html', context=context)


@login_required
def del_ursaff_item(request, item):

    if not request.user.is_staff:
        messages.error(request, "Vous n'avez pas les droits suffisants pour accéder à cette page")
        return redirect('frais')

    a = ursaffModel.objects.get(annee=item)
    a.delete()

    return redirect('ursaff')


@login_required
def new_ursaff_item(request):

    if not request.user.is_staff:
        messages.error(request, "Vous n'avez pas les droits suffisants pour accéder à cette page")
        return redirect('frais')

    context = {}

    list_taux = ursaffModel.objects.all()
    context['list_taux'] = list_taux
    an = list_taux.last().annee + 1
    form = newUrsaffForm(initial={'annee': an})

    if request.method == 'POST':
        form = newUrsaffForm(request.POST)

    if form.is_valid():
        form.save()
        return redirect('ursaff')

    context['form'] = form
    context['new'] = True

    # return render(request, 'frais/ursaff_new.html', context=context)
    return render(request, 'frais/ursaff.html', context=context)


def jsonTodb(file):

    with open(file, 'r') as f:
        data = json.load(f)

    for element in data.keys():
        for x in data[element].keys():
            print(x)
            repas = data[element][x]['R']
            nuit = data[element][x]['N+PD']

            print(element, x, repas, nuit)


def dict_to_db(elements):

    for element in elements:
        Bareme.objects.create(**element)
        # print(element)
    return len(elements)


@login_required
def new_bareme_item(request):

    if not request.user.is_staff:
        messages.error(request, "Vous n'avez pas les droits suffisants pour accéder à cette page")
        return redirect('frais')

    context = {}
    an = Bareme.objects.last().annee + 1
    context['an'] = an
    success = True
    if request.method == 'POST' and request.FILES['file']:

        an = request.POST.get('annee')

        if Bareme.objects.filter(annee=an).count() != 0:
            messages.error(request, f"l'année {an} existe déjà")
            success = False
            context['an'] = an
            # return redirect('frais')
        else:
            file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)

            uploaded_file_url = fs.url(filename)
            uploaded_file_path = fs.path(filename)
            datas = parse_xl.xlsx_to_db(uploaded_file_path, an)

            success = True
            nb_enr = dict_to_db(datas)

            context['success'] = success
            messages.success(request, f"{nb_enr} nouvelles entrées pour l'année {an} ont été ajoutées")

            return redirect('frais')

    context['success'] = success
    return render(request, 'frais/bareme_new.html', context=context)


@login_required
def del_bareme(request):

    if not request.user.is_staff:
        messages.error(request, "Vous n'avez pas les droits suffisants pour accéder à cette page")
        return redirect('frais')

    context = {}

    b = Bareme.objects.all()
    datas = []
    annees = {element.annee for element in b}
    context['annees'] = annees
    for an in annees:
        n = Bareme.objects.filter(annee=an).count()
        datas.append((an, n))
    context['datas'] = datas

    return render(request, 'frais/bareme_del.html', context=context)


@login_required
def del_bareme_item(request, item):

    if not request.user.is_staff:
        messages.error(request, "Vous n'avez pas les droits suffisants pour accéder à cette page")
        return redirect('frais')

    Bareme.objects.filter(annee=item).delete()
    messages.success(request, f"Les données de l'année {item} ont été supprimées")

    return redirect('bareme_item')
