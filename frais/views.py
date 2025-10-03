from pathlib import Path
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import json
from django.shortcuts import render, redirect

from frais.decorators import user_is_staff
from utilproject.settings import MEDIA_ROOT
from .forms import FraisForm, updateUrsaffForm, newUrsaffForm
from frais.models import ursaffModel, Bareme
from datetime import date
from frais import parse_xl

from utilproject.settings import MEDIA_ROOT
from .import_bareme_cmd import  import_bareme_csv # convert_pdf2csv


def frais(request):

    bareme_total = Bareme.objects.filter(annee=date.today().year)
    taux_ursaff = ursaffModel.objects.filter(annee=date.today().year)

    if bareme_total.count() == 0:
        annee_bareme = Bareme.objects.last().annee
    else:
        annee_bareme = date.today().year
    print(annee_bareme)
    return redirect('frais_an', annee_bareme)
#     return redirect('frais_an', an=annee_bareme)


def frais_an(request, an):

    # list_taux = ursaffModel.objects.get(annee=an)
    list_taux = ursaffModel.objects.all()[0]
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


@user_is_staff
@login_required
def maj_ursaff(request):

    # if not request.user.is_staff:
    #     messages.error(request, "Vous n'avez pas les droits suffisants pour accéder à cette page")
    #     return redirect('frais')

    context = {}
    list_taux = ursaffModel.objects.all()
    context['list_taux'] = list_taux
    context['new'] = False

    return render(request, 'frais/ursaff.html', context=context)


@user_is_staff
@login_required
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
        context['new'] = False
        return render(request, 'frais/ursaff_update.html', context=context)

    context['form'] = form

    return render(request, 'frais/ursaff_update.html', context=context)


@user_is_staff
@login_required
def del_ursaff_item(request, item):

    a = ursaffModel.objects.get(annee=item)
    a.delete()

    return redirect('ursaff')


@user_is_staff
@login_required
def new_ursaff_item(request):

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
            repas = data[element][x]['R']
            nuit = data[element][x]['N+PD']

            print(element, x, repas, nuit)


def dict_to_db(elements):

    for element in elements:
        Bareme.objects.create(**element)
        # print(element)
    return len(elements)



@user_is_staff
@login_required
def new_bareme_item(request):
    """Vue pour l'upload et le traitement des fichiers PDF/CSV de barème"""

    context = {}
    an = Bareme.objects.last().annee + 1
    context['an'] = an

    if request.method == 'GET':
        # Affichage du formulaire
        return render(request, 'frais/bareme_new.html', context=context)

    elif request.method == 'POST':
        # Vérifier si c'est une requête AJAX
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        try:
            an = request.POST.get('annee')

            # Vérifier si l'année existe déjà
            if Bareme.objects.filter(annee=an).count() != 0:
                error_msg = f"L'année {an} existe déjà"

                if is_ajax:
                    return JsonResponse({
                        'success': False,
                        'error': error_msg
                    })
                else:
                    messages.error(request, error_msg)
                    context['an'] = an
                    return render(request, 'frais/bareme_new.html', context=context)

            # Vérifier qu'un fichier est fourni
            if 'file' not in request.FILES:
                error_msg = "Aucun fichier fourni"

                if is_ajax:
                    return JsonResponse({
                        'success': False,
                        'error': error_msg
                    })
                else:
                    messages.error(request, error_msg)
                    context['an'] = an
                    return render(request, 'frais/bareme_new.html', context=context)

            file = request.FILES['file']

            # Sauvegarder le fichier PDF
            location = Path(MEDIA_ROOT / 'pdf')
            fs = FileSystemStorage(location=location)
            filename = fs.save(file.name, file)
            uploaded_file_path = fs.path(filename)
            origin = MEDIA_ROOT / 'pdf' / uploaded_file_path
            dest = MEDIA_ROOT / 'csv' / 'bareme.csv'

            # Convertir le PDF en CSV
            # convert_pdf2csv(origin=origin, dest=dest)

            # Importer les données CSV
            result = import_bareme_csv()

            nb_enr = Bareme.objects.filter(annee=an).count()
            success_msg = f"{nb_enr} nouvelles entrées pour l'année {an} ont été ajoutées"

            if is_ajax:
                # Retourner une réponse JSON pour AJAX
                return JsonResponse({
                    'success': True,
                    'created': result['created'],
                    'updated': result['updated'],
                    'incomplete': result['incomplete'],
                    'erreurs': result.get('erreurs', []),
                    'nb_enr': nb_enr,
                    'annee': an,
                    'message': success_msg
                })
            else:
                # Retourner une page HTML classique
                messages.success(request, success_msg)
                return redirect('bareme_item')

        except Exception as e:
            error_msg = f"Erreur lors de l'import : {str(e)}"

            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': error_msg
                })
            else:
                messages.error(request, error_msg)
                context['an'] = request.POST.get('annee', an)
                return render(request, 'frais/bareme_new.html', context=context)


@user_is_staff
@login_required
def del_bareme(request):

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


@user_is_staff
@login_required
def del_bareme_item(request, item):

    Bareme.objects.filter(annee=item).delete()
    messages.success(request, f"Les données de l'année {item} ont été supprimées")

    return redirect('bareme_item')



if __name__ == '__main__':
    pass