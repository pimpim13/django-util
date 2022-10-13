from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView

from snb.models import Snb_ref, Coeff, Inflation
from snb.forms import SnbUpdateForm, SnbCreateForm, CalculSalaireForm
from frais.parse_xl import populate_nr


def snb(request):

    if not Coeff.objects.all():
        populate_db_nr()

    datachart = chart()
    print(datachart)

    context = {}
    evol_snb = "0.3"
    inflation = "5.1"
    form = CalculSalaireForm()
    if request.method == 'POST':
        form = CalculSalaireForm(request.POST)
        if form.is_valid():
            annee_previous = int(form.cleaned_data['annee']) - 1
            annee_next = int(form.cleaned_data['annee']) + 1

            snb = float(Snb_ref.objects.get(annee=form.cleaned_data['annee']).snb)

            snb_previous = float(Snb_ref.objects.get(annee=annee_previous).snb)
            Nr = float(form.cleaned_data['Nr'])
            echelon = float(form.cleaned_data['echelon'])
            maj_res = float(form.cleaned_data['maj_res'])
            tps_trav = float(form.cleaned_data['tps_trav'])
            # Nr_futur = float(form.cleaned_data['Nr_futur'])
            # echelon_futur = float(form.cleaned_data['echelon_futur'])
            # inflation = float(form.cleaned_data['inflation'])/100 + 1.0

            evol_snb = request.POST.get('evol_snb')
            fl_evol_snb = float(evol_snb)
            snb_futur = snb * (fl_evol_snb/100 + 1)

            inflation = request.POST.get('inflation')
            fl_evol_inflation = float(inflation)/100 + 1

            salaire = calculate_mensuel(Nr=Nr,
                                        echelon=echelon,
                                        maj_res=maj_res,
                                        tps_trav=tps_trav,
                                        snb=snb)

            # salaire_futur = calculate_mensuel(Nr=Nr_futur,
            #   echelon=echelon_futur,
            #   maj_res=maj_res,
            #   tps_trav=tps_trav,
            #   snb=snb_futur)

            salaire_futur = calculate_mensuel(Nr=Nr,
                                              echelon=echelon,
                                              maj_res=maj_res,
                                              tps_trav=tps_trav,
                                              snb=snb_futur)

            salaire_annuel = round(salaire * 13, 2)
            salaire_futur_annuel = round(salaire_futur * 13, 2)
            salaire_annuel_net = round(salaire_annuel * 0.75, 2)
            salaire_futur_annuel_net = round(salaire_futur_annuel * 0.75, 2)

            perte_brute = calculate_perte(salaire, salaire_futur, fl_evol_inflation)
            # perte_brute = calculate_perte(salaire, salaire, fl_evol_inflation)
            perte = round(perte_brute * 0.75, 2)

            context['annee'] = form.cleaned_data['annee']
            context['annee_next'] = annee_next
            context['annee_previous'] = annee_previous
            context['salaire'] = salaire
            context['salaire_annuel'] = salaire_annuel

            context['salaire_futur'] = salaire_futur
            context['salaire_annuel_futur'] = salaire_futur_annuel
            context['snb'] = snb
            context['snb_previous'] = snb_previous
            context['evol_snb'] = evol_snb
            context['perte_brute'] = perte_brute
            context['perte'] = perte

    context['form'] = form
    context['evol_snb'] = evol_snb
    context['inflation'] = inflation
    context['variation_snb'] = datachart.get('variation_snb', [])
    context['labelchart'] = datachart.get('annees', [])
    context['inflation_chart'] = datachart.get('inflation', [])

    return render(request, 'snb/snb.html/', context=context)


class SnbListView(ListView):

    model = Snb_ref
    template_name = 'snb/snb_update.html'
    context_object_name = 'list_snb'


# def snb_list(request):
#     context = {}
#     list_snb = Snb_ref.objects.all()
#     context['list_snb'] = list_snb
#     context['maj'] = False
#
#     return render(request, 'snb/snb_update.html', context=context)


class SnbUpdate(UpdateView):
    model = Snb_ref
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

    list_snb = Snb_ref.objects.all()
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
    Snb_ref.objects.get(annee=item).delete()
    return redirect('snb_list')


def populate_db_nr():
    datas = populate_nr()
    for data in datas:
        Coeff.objects.create(**data)


def calculate_mensuel(snb=0.0, Nr=0.0, echelon=0.0,  maj_res=0.0, tps_trav=0.0, annee=0):
    return round(snb * Nr * echelon * maj_res * tps_trav / 100, 2)


def calculate_perte(salaire, salaire_futur, inflation):
    """ coeff de 0.75 pour évaluer la perte nette """
    return round(13 * ((salaire_futur * 1) - (salaire * 1) * inflation), 2)


def chart():
    queryset = Snb_ref.objects.order_by('annee')
    annees = [_.annee for _ in queryset]
    datas = [_.snb for _ in queryset]

    inflation = [round(_.valeur * 100,1) for _ in Inflation.objects.order_by('annee')]
    variation = [round(((datas[n+1]/datas[n])-1)*100, 1) for n in range(len(datas)-1)]
    inflation[0] = 0
    variation.insert(0, 0)

    return {'annees': annees, 'datas': datas, 'inflation': inflation, 'variation_snb': variation}


