from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView

from snb.models import Snb_ref, Inflation, Coeff_New, Snb_ref_New
from snb.forms import SnbUpdateForm, SnbCreateForm, CalculSalaireForm, EvolSnbForm
from frais.parse_xl import populate_nr


def snb(request):

    if not Coeff_New.objects.all():
        populate_db_nr()

    context = {}
    evol_snb = "0.3"
    inflation = "5.1"
    form = CalculSalaireForm()
    if request.method == 'POST':
        form = CalculSalaireForm(request.POST)
        if form.is_valid():
            annee_previous = int(form.cleaned_data['date_application'][:4]) - 1
            annee_next = int(form.cleaned_data['date_application'][:4]) + 1

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
            perte = round(perte_brute * 0.75, 2)

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

#
# def snb_update_item(request, item):
#
#     context = {'an': item}
#     success = False
#     list_snb = Snb_ref.objects.all()
#     context['list_snb'] = list_snb
#
#     snb_an = Snb_ref.objects.get(annee=item)
#     print(item)
#
#     if request.method == 'POST':
#
#         form = SnbUpdateForm(request.POST, instance=snb_an)
#         # form.annee = snb_an.annee
#         if form.is_valid():
#             print(form.cleaned_data)
#             form.save()
#             context['maj'] = False
#             return redirect('snb_list')
#
#     else:
#         form = SnbUpdateForm(instance=snb_an)
#
#     context['success'] = success
#     context['form'] = form
#     context['maj'] = True
#     context['new'] = False
#
#     # return render(request, 'frais/ursaff_new.html', context=context)
#     return render(request, 'snb/snb_update.html', context=context)


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

    context = {}

    form = EvolSnbForm()
    if request.method == 'POST':
        form = EvolSnbForm(request.POST)
        if form.is_valid():
            date1 = '2022-01-01'
            date2 = '2022-07-01'
            date3 = '2023-01-01'

            snb1 = float(Snb_ref_New.objects.filter(date_application=date1)[0].snb)
            snb2 = float(Snb_ref_New.objects.filter(date_application=date2)[0].snb)
            snb3 = float(Snb_ref_New.objects.filter(date_application=date3)[0].snb)

            nr = form.cleaned_data['Nr']
            coeff_nr1 = Coeff_New.objects.filter(date_application__lte=date1, NR=nr)[0].valeur
            coeff_nr2 = Coeff_New.objects.filter(date_application__lte=date2, NR=nr)[0].valeur
            coeff_nr3 = Coeff_New.objects.filter(date_application__lte=date3, NR=nr)[0].valeur
            print(coeff_nr1, snb1)
            print(coeff_nr2, snb2)
            print(coeff_nr3, snb3)

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
            context['gain_2023'] = round((salaire3 - salaire2) * 13, 2)

    context['form'] = form

    return render(request, 'snb/snb_evol.html/', context=context)