from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView
from pandas.core.dtypes.cast import astype_array

from snb.models import Snb_ref, Inflation, Coeff_New, Snb_ref_New
from snb.forms import SnbUpdateForm, SnbCreateForm, CalculSalaireForm, EvolSnbForm, TranspositionForm
from frais.parse_xl import populate_nr
from snb.api_snb import create_table, test as pdf_gen, spumoni

from datetime import datetime

EVOL_SNB = "2"    # valeur par défaut du curseur d'évolution du SNB
INFLATION = "5.1"  # valeur par défaut du curseur d'évolution de l'inflation
TAUX_BRUT_NET = 0.75  # valeur par défaut du niveau de charges sociales


def snb(request):

    if not Coeff_New.objects.all():
        populate_db_nr()

    context = {}
    # evol_snb = "0.3"
    evol_snb = EVOL_SNB
    inflation = INFLATION
    # inflation = "5.1"
    form = CalculSalaireForm()
    if request.method == 'POST':
        form = CalculSalaireForm(request.POST)
        if form.is_valid():
            annee_previous = int(form.cleaned_data['date_application'][:4]) - 1
            annee_next = int(form.cleaned_data['date_application'][:4]) + 1

            print('annee_previous', annee_previous)
            print('annee_next', annee_next)

            snb = float(Snb_ref_New.objects.filter(date_application=form.cleaned_data['date_application'])[0].snb)
            date_application = Snb_ref_New.objects.filter(date_application=form.cleaned_data['date_application'])[0].date_application
            if Snb_ref_New.objects.last().annee > annee_previous:
                annee_previous = int(form.cleaned_data['date_application'][:4])

            nr = form.cleaned_data['Nr']
            coeff_nr = Coeff_New.objects.filter(date_application__lte=date_application, NR=nr)[0].valeur
            print(coeff_nr)

            echelon = float(form.cleaned_data['echelon'])
            maj_res = float(form.cleaned_data['maj_res'])
            tps_trav = float(form.cleaned_data['tps_trav'])

            evol_snb = request.POST.get('evol_snb')
            fl_evol_snb = float(evol_snb)
            snb_futur = snb * (fl_evol_snb/100 + 1)

            inflation = request.POST.get('inflation')
            fl_evol_inflation = float(inflation)/100 + 1

            salaire = calculate_mensuel(Nr=coeff_nr,
                                        echelon=echelon,
                                        maj_res=maj_res,
                                        tps_trav=tps_trav,
                                        snb=snb)

            salaire_futur = calculate_mensuel(Nr=coeff_nr,
                                              echelon=echelon,
                                              maj_res=maj_res,
                                              tps_trav=tps_trav,
                                              snb=snb_futur)

            salaire_annuel = round(salaire * 13, 2)
            salaire_futur_annuel = round(salaire_futur * 13, 2)

            perte_brute = calculate_perte(salaire, salaire_futur, fl_evol_inflation)
            perte = round(perte_brute * TAUX_BRUT_NET, 2)

            context['annee'] = form.cleaned_data['date_application'][:4]
            context['annee_next'] = annee_next
            context['annee_previous'] = annee_previous
            context['salaire'] = salaire
            context['salaire_annuel'] = salaire_annuel

            context['salaire_futur'] = salaire_futur
            context['salaire_annuel_futur'] = salaire_futur_annuel
            context['snb'] = snb
            context['date_application'] = date_application
            context['evol_snb'] = evol_snb
            context['perte_brute'] = perte_brute
            context['perte'] = perte

    context['form'] = form
    context['evol_snb'] = evol_snb
    context['inflation'] = inflation

    return render(request, 'snb/snb.html/', context=context)


class SnbListView(ListView):
    model = Snb_ref_New
    template_name = 'snb/snb_update.html'
    context_object_name = 'list_snb'


class SnbUpdate(UpdateView):
    model = Snb_ref_New
    form_class = SnbUpdateForm
    template_name = 'snb/snb_update.html'
    success_url = reverse_lazy('snb_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['maj'] = True
        # context['new'] = False
        context['list_snb'] = Snb_ref.objects.all()
        return context


def snb_new(request):

    context = {}

    list_snb = Snb_ref_New.objects.all()
    context['list_snb'] = list_snb

    form = SnbCreateForm()

    if request.method == 'POST':
        form = SnbCreateForm(request.POST)

    if form.is_valid():
        form.save()
        success = True
        return redirect('snb_list')
    else:
        success = False

    context['success'] = success
    context['form'] = form
    context['maj'] = True
    context['new'] = True
    # pdf_view(request)
    # return render(request, 'frais/ursaff_new.html', context=context)
    return render(request, 'snb/snb_update.html', context=context)


def snb_delete_item(request, item):
    Snb_ref_New.objects.get(annee=item).delete()
    return redirect('snb_list')


def populate_db_nr():
    datas = populate_nr()
    for data in datas:
        Coeff_New.objects.create(**data)


def calculate_mensuel(snb=0.0, Nr=0.0, echelon=0.0,  maj_res=0.0, tps_trav=0.0, annee=0):
    return round(snb * Nr * echelon * maj_res * tps_trav / 100, 2)


def calculate_perte(salaire, salaire_futur, inflation):
    """ coeff de 0.75 pour évaluer la perte nette """
    return round(13 * ((salaire_futur * 1) - (salaire * 1) * inflation), 2)


def snb_evol(request):

    # DATE_1 = '2021-01-01'
    # DATE_2 = '2022-07-01'
    # DATE_3 = '2023-01-01'


    DATE_1 = Snb_ref_New.objects.all()[2].date_application
    DATE_2 = Snb_ref_New.objects.all()[1].date_application
    DATE_3 = Snb_ref_New.objects.all()[0].date_application


    context = {}
    form = EvolSnbForm()
    if request.method == 'POST':
        form = EvolSnbForm(request.POST)
        if form.is_valid():

            snb1 = float(Snb_ref_New.objects.filter(date_application=DATE_1)[0].snb)
            snb2 = float(Snb_ref_New.objects.filter(date_application=DATE_2)[0].snb)
            snb3 = float(Snb_ref_New.objects.filter(date_application=DATE_3)[0].snb)

            nr = form.cleaned_data['Nr']
            coeff_nr1 = Coeff_New.objects.filter(date_application__lte=DATE_1, NR=nr)[0].valeur
            coeff_nr2 = Coeff_New.objects.filter(date_application__lte=DATE_2, NR=nr)[0].valeur
            coeff_nr3 = Coeff_New.objects.filter(date_application__lte=DATE_3, NR=nr)[0].valeur

            echelon = float(form.cleaned_data['echelon'])
            maj_res = float(form.cleaned_data['maj_res'])
            tps_trav = float(form.cleaned_data['tps_trav'])

            salaire1 = round(calculate_mensuel(Nr=coeff_nr1,
                                               echelon=echelon,
                                               maj_res=maj_res,
                                               tps_trav=tps_trav,
                                               snb=snb1), 2)

            salaire2 = calculate_mensuel(Nr=coeff_nr2,
                                         echelon=echelon,
                                         maj_res=maj_res,
                                         tps_trav=tps_trav,
                                         snb=snb2)

            salaire3 = calculate_mensuel(Nr=coeff_nr3,
                                         echelon=echelon,
                                         maj_res=maj_res,
                                         tps_trav=tps_trav,
                                         snb=snb3)

            salaire_annuel1 = round(salaire1 * 13, 2)
            salaire_annuel2 = round(salaire2 * 13, 2)
            salaire_annuel3 = round(salaire3 * 13, 2)

            context['salaire1'] = salaire1
            context['salaire2'] = salaire2
            context['salaire3'] = salaire3

            context['salaire_annuel1'] = salaire_annuel1
            context['salaire_annuel2'] = salaire_annuel2
            context['salaire_annuel3'] = salaire_annuel3

            context['ecart_1_2'] = salaire2 - salaire1
            context['ecart_2_3'] = salaire3 - salaire2

            context['ecart_2022'] = round((salaire2 - salaire1) * 6.5, 2)
            context['ecart_mensuel_2022'] = round((salaire2 - salaire1), 2)
            context['gain_2023'] = round((salaire3 - salaire2) * 13, 2)

            context['data1'] = [salaire1]
            context['data2'] = [salaire2]
            context['data3'] = [salaire3]
            # context['data2'] = [salaire_annuel1, salaire_annuel2, salaire_annuel3]

    context['form'] = form

    return render(request, 'snb/snb_evol.html/', context=context)


def compute(request):
    DATE_1 = '2021-01-01'
    DATE_2 = '2022-07-01'
    DATE_3 = '2023-01-01'

    date1 = DATE_1
    date2 = DATE_2
    date3 = DATE_3

    context = {}

    snb1 = float(Snb_ref_New.objects.filter(date_application=date1)[0].snb)
    snb2 = float(Snb_ref_New.objects.filter(date_application=date2)[0].snb)
    snb3 = float(Snb_ref_New.objects.filter(date_application=date3)[0].snb)

    nr = request.POST.get('Nr', 30)
    coeff_nr1 = Coeff_New.objects.filter(date_application__lte=date1, NR=nr)[0].valeur
    coeff_nr2 = Coeff_New.objects.filter(date_application__lte=date2, NR=nr)[0].valeur
    coeff_nr3 = Coeff_New.objects.filter(date_application__lte=date3, NR__gte=nr)[0].valeur
    coeff_nr_sup = Coeff_New.objects.filter(date_application__lte=date3, NR__gte=nr)[1].valeur
    nr_sup = Coeff_New.objects.filter(date_application__lte=date3, NR__gte=nr)[1].NR

    echelon = float(request.POST.get('echelon', 4.0))
    maj_res = float(request.POST.get('maj_res', 24.0))
    tps_trav = float(request.POST.get('tps_trav', 1.0))


    salaire1 = round(calculate_mensuel(Nr=coeff_nr1,
                                       echelon=echelon,
                                       maj_res=maj_res,
                                       tps_trav=tps_trav,
                                       snb=snb1), 2)

    salaire2 = calculate_mensuel(Nr=coeff_nr2,
                                 echelon=echelon,
                                 maj_res=maj_res,
                                 tps_trav=tps_trav,
                                 snb=snb2)

    salaire3 = calculate_mensuel(Nr=coeff_nr3,
                                 echelon=echelon,
                                 maj_res=maj_res,
                                 tps_trav=tps_trav,
                                 snb=snb3)

    salaire4 = calculate_mensuel(Nr=coeff_nr_sup,
                                 echelon=echelon,
                                 maj_res=maj_res,
                                 tps_trav=tps_trav,
                                 snb=snb3)


    p27orTalon = round(salaire4 * 0.027 if salaire4 * 0.027 >= 100 else 100, 2)
    p27 = round(salaire4 * 0.027, 2)

    salaire5 = salaire4 + p27orTalon

    salaire_annuel1 = round(salaire1 * 13, 2)
    salaire_annuel2 = round(salaire2 * 13, 2)
    salaire_annuel3 = round(salaire3 * 13, 2)

    context['salaire1'] = salaire1  # salaire mensuel au 01/01/2022
    context['salaire2'] = salaire2  # salaire mensuel au 01/07/2022
    context['salaire3'] = salaire3  # salaire mensuel au 01/01/2023 après mesures de branche
    context['salaire4'] = salaire4  # salaire mensuel au 01/01/2023 après mesures salariales Rte avant prime

    context['nr_sup'] = nr_sup

    context['salaire_annuel1'] = salaire_annuel1
    context['salaire_annuel2'] = salaire_annuel2
    context['salaire_annuel3'] = salaire_annuel3

    context['ecart_1_2'] = salaire2 - salaire1
    context['ecart_2_3'] = salaire3 - salaire2
    context['ecart_4_3'] = salaire4 - salaire3
    context['p27'] = p27
    context['p27orTalon'] = p27orTalon

    context['ecart_pourcent_2023_2022'] = round((salaire3/salaire2)*100 - 100, 2)
    context['salaire5'] = round(salaire5, 2) # salaire mensuel total au 01/01/2023
    context['total_evolution'] = round(salaire5 - salaire1, 2)

    context['ecart_2022'] = round((salaire2 - salaire1) * 6.5, 2)
    context['ecart_mensuel_2022'] = round((salaire2 - salaire1), 2)

    context['data1'] = [salaire1]
    context['data2'] = [round(salaire2 - salaire1, 2)]
    context['data3'] = [round(salaire3 - salaire2, 2)]
    context['data4'] = [round(salaire5 - salaire3, 2)]
    context['gain_2023'] = round((salaire3 - salaire1), 2)
    context['ecart_mensuel_2023'] = round((salaire3 - salaire2), 2)
    context['gain_total'] = round((salaire3 - salaire1), 2)
    context['pourcent_total'] = round((salaire3 / salaire1) * 100 - 100, 2)
    context['totalPourcent2322'] = round((salaire5 / salaire1) * 100 - 100, 2)
    context['totalPourcentRte'] = round((salaire5 / salaire3) * 100 - 100, 2)

    return JsonResponse(context)

def snb_transpose(request):

    form = TranspositionForm()
    context = {'form': form}

    return render(request, 'snb/snb_transposition.html/', context = context)


def transpose_compute(request):

    DATE1 = Snb_ref_New.objects.first().date_application
    context = {}

    nr = request.POST.get('Nr', 130)
    echelon = float(request.POST.get('echelon', 7.0))
    maj_res = float(request.POST.get('maj_res', 25.0))
    tps_trav = float(request.POST.get('tps_trav', 1.0))


    coeff_nr1 = Coeff_New.objects.filter(date_application__lte=DATE1, NR=nr)[0].valeur

    snb1 = float(Snb_ref_New.objects.filter(date_application=DATE1)[0].snb)

    coeff_nr_sup = Coeff_New.objects.filter(date_application__lte=DATE1, NR__gte=nr)[1].valeur
    nr_sup = Coeff_New.objects.filter(date_application__lte=DATE1, NR__gte=nr)[1].NR

    coeff_2nr_sup = Coeff_New.objects.filter(date_application__lte=DATE1, NR__gte=nr_sup)[1].valeur
    nr2_sup = Coeff_New.objects.filter(date_application__lte=DATE1, NR__gte=nr_sup)[1].NR


    salaire_tp = round(calculate_mensuel(Nr=coeff_nr1,
                                       echelon=echelon,
                                       maj_res=maj_res,
                                       tps_trav=1,
                                       snb=snb1), 2)

    salaire1 = round(calculate_mensuel(Nr=coeff_nr1,
                                       echelon=echelon,
                                       maj_res=maj_res,
                                       tps_trav=tps_trav,
                                       snb=snb1), 2)

    salaire_nr_sup = round(calculate_mensuel(Nr=coeff_nr_sup,
                                       echelon=echelon,
                                       maj_res=maj_res,
                                       tps_trav=tps_trav,
                                       snb=snb1), 2)

    salaire_2nr_sup = round(calculate_mensuel(Nr=coeff_2nr_sup,
                                       echelon=echelon,
                                       maj_res=maj_res,
                                       tps_trav=tps_trav,
                                       snb=snb1), 2)


    p27orTalon = salaire_tp * 0.027 if salaire_tp * 0.027 >= 100 else 100
    p27 = salaire1 * 0.027


    annuel1 = round((salaire1 * 13) + (p27orTalon * 12), 2)
    annuel_nr_sup = round(salaire_nr_sup * 13,2)
    annuel_2nr_sup = round(salaire_2nr_sup * 13, 2)


    if annuel_2nr_sup != annuel_nr_sup:
        msg="..."
        if annuel_2nr_sup <= annuel1:
            nb_nr = 2
            annuel_nr = annuel_2nr_sup
        else:
            nb_nr = 1
            annuel_nr = annuel_nr_sup
    else:
        msg = "Vous avez atteint la butée de NR"

        if nr == "370":
            nb_nr = 0
            annuel_nr = annuel_nr_sup
            msg += ' Vous conservez la prime de 2,7%'

        elif nr == "365":
            nb_nr = 1
            annuel_nr = annuel_nr_sup

        elif nr_sup == "370":
            nb_nr = 1
            annuel_nr = annuel_nr_sup


    residu_annuel = round(annuel1 - annuel_nr, 2)
    nr_sup = Coeff_New.objects.filter(date_application__lte=DATE1, NR__gte=nr)[nb_nr].NR
    taux_residuel = residu_annuel/annuel_nr

    if nr == "370": # Traitement du cas NR 3770 qy-ui conserve la prime
        taux_residuel_arrrondi = 0.027
    else: # traitement de tous les autres cas
        taux_residuel_arrrondi = int((taux_residuel*1000)+1)/1000

    prime_annuelle = round(annuel_nr * taux_residuel_arrrondi,2)


    context['nr1'] = nr
    context['mensuel1'] = salaire1
    context['mensuel_tp'] = salaire_tp
    context['p27'] = round(p27orTalon,2)
    context['annuel1'] = annuel1
    context['annuel_nr'] = annuel_nr
    context['nb_nr'] = nb_nr
    context['nr_sup'] = nr_sup
    context['taux_residuel_arrondi'] = str(round(taux_residuel_arrrondi*100,2)) +'%'
    context['residu_annuel'] = residu_annuel
    context['prime_annuelle'] = prime_annuelle
    context['msg'] = msg


    return JsonResponse(context)


def test(request):

    pdf_gen()
    texte = f"pdf généré à {datetime.now()}"


    return HttpResponse(texte)
