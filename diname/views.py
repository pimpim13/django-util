from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from snb.models import Snb_ref_New, Coeff_New, Echelon
from diname.models import Site, Famille, Attractivite

from snb.api_snb import calcul_salaire_mensuel
from diname.forms import DinameForm

DATE = '2023-01-01'  # A REVOIR

NR_PLANCHER = 130
NR_PLAFOND = 280
ECH_PLANCHER = 4
ECH_PLAFOND = 7
context = {}


def diname(request):

    context = {}
    form = DinameForm()

    if request.method == 'POST':
        form = DinameForm(request.POST)

        if form.is_valid():
            print('toto')
            snb1 = float(Snb_ref_New.objects.filter(date_application=DATE)[0].snb)
            nr = form.cleaned_data['Nr']

            coeff_nr1 = Coeff_New.objects.filter(date_application__lte=DATE, NR=nr)[0].valeur
            coeff_nr_plancher = Coeff_New.objects.filter(date_application__lte=DATE, NR=NR_PLANCHER)[0].valeur
            coeff_nr_plafond = Coeff_New.objects.filter(date_application__lte=DATE, NR=NR_PLAFOND)[0].valeur

            echelon = float(form.cleaned_data['echelon'])
            echelon_plancher = Echelon.objects.get(echelon=ECH_PLANCHER).coeff
            echelon_plafond = Echelon.objects.get(echelon=ECH_PLAFOND).coeff

            maj_res = float(form.cleaned_data['maj_res'])
            tps_trav = float(form.cleaned_data['tps_trav'])

            salaire1 = round(calcul_salaire_mensuel(coeff=coeff_nr1,
                                                    ech=echelon,
                                                    maj_res=maj_res,
                                                    tps_trav=tps_trav,
                                                    snb=snb1), 2)

            plancher = round(calcul_salaire_mensuel(coeff=coeff_nr_plancher,
                                                    ech=echelon_plancher,
                                                    maj_res=1.24,
                                                    tps_trav=1,
                                                    snb=snb1), 2)
            plafond = round(calcul_salaire_mensuel(coeff=coeff_nr_plafond,
                                                    ech=echelon_plafond,
                                                    maj_res=1.24,
                                                    tps_trav=1,
                                                    snb=snb1), 2)

            ind_art30 = round(salaire1 * 2, 2) * form.cleaned_data['art30']
            # if form.cleaned_data['art30'] == False:
            #     print('il passe par là')
            #     ind_art30 = 0
            #     print(ind_art30)

            surface = form.cleaned_data['famille']
            loyer_origine = Site.objects.get(localisation=form.cleaned_data['site_origine']).loyer
            loyer_destination = Site.objects.get(localisation=form.cleaned_data['site_destination']).loyer

            ecart_loyer = round(max((loyer_destination - loyer_origine), 0), 2)
            indemnisation_ecart_loyer = round(ecart_loyer * 12 * 5 * float(surface), 2)
            base_diname = min(max(plancher, salaire1), plafond)
            prime_amg = base_diname * 5
            context['attractivite'] = "bg-secondary"

            attractivite = Site.objects.get(localisation=form.cleaned_data['site_destination']).attractivite.couleur
            moisMGES = Site.objects.get(localisation=form.cleaned_data['site_destination']).attractivite.mois
            lbl_MGES = Site.objects.get(localisation=form.cleaned_data['site_destination']).attractivite.lbl_MGES

            prime_MGES = round(base_diname * moisMGES, 2)
            context['mois_MGEE'] = 0
            prime_MGEE = 0

            if form.cleaned_data['eligible_MGEE']:
                if form.cleaned_data['art30']:
                    prime_MGEE = round(base_diname * 2, 2)
                    context['mois_MGEE'] = 2
                else:
                    prime_MGEE = base_diname
                    context['mois_MGEE'] = 1


            context['form'] = form
            context["salaire_mensuel"] = salaire1
            context['ind_art30'] = ind_art30
            context['surface'] = surface
            context["loyer_origine"] = loyer_origine
            context["loyer_destination"] = loyer_destination
            context["ecart_loyer"] = ecart_loyer
            context['plancher'] = plancher
            context['plafond'] = plafond
            context['base_diname'] = base_diname
            context['indemnisation_loyer'] = indemnisation_ecart_loyer
            context['prime_amg'] = prime_amg
            context['attractivite'] = attractivite
            context['moisMGES'] = moisMGES
            context['lbl_MGES'] = lbl_MGES
            context['prime_MGES'] = prime_MGES
            context['prime_MGEE'] = prime_MGEE

    context["form"] = form

    return render(request, 'diname/diname.html/', context=context)

