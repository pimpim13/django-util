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

    context['attractivite'] = "bg-secondary"
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
                                                    maj_res=1.25,
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
            indemnisation_ecart_loyer = round(ecart_loyer * 12 * 5 * float(surface), 2) * form.cleaned_data['eligible_AMG']
            base_diname = min(max(plancher, salaire1), plafond)
            prime_amg = base_diname * 5 * form.cleaned_data['eligible_AMG']

            attractivite = Site.objects.get(localisation=form.cleaned_data['site_destination']).attractivite.couleur
            moisMGES = Site.objects.get(localisation=form.cleaned_data['site_destination']).attractivite.mois
            lbl_MGES = Site.objects.get(localisation=form.cleaned_data['site_destination']).attractivite.lbl_MGES

            prime_MGES = round(base_diname * moisMGES, 2) * form.cleaned_data['eligible_AMG']
            # prime_MGES_ = f"{prime_MGES:9.2f}"
            context['mois_MGEE'] = 0
            prime_MGEE = 0

            if form.cleaned_data['eligible_MGEE']:
                if form.cleaned_data['art30']:
                    prime_MGEE = round(base_diname * 2, 2)
                    context['mois_MGEE'] = 2
                else:
                    prime_MGEE = base_diname
                    context['mois_MGEE'] = 1
            total_diname = prime_amg + indemnisation_ecart_loyer + prime_MGES + prime_MGEE
            total_diname_an = round(min(total_diname/5, 20000), 2)
            total_general = min(total_diname, 100000) + ind_art30

            context['form'] = form
            context["salaire_mensuel"] = f"{salaire1:9.2f}"
            context['ind_art30'] = f"{ind_art30:9.2f}"
            context['surface'] = surface
            context["loyer_origine"] = f"{loyer_origine:9.2f}"
            context["loyer_destination"] = f"{loyer_destination:9.2f}"
            context["ecart_loyer"] = f"{ecart_loyer:9.2f}"
            context['plancher'] = f"{plancher:9.2f}"
            context['plafond'] = f"{plafond:9.2f}"
            context['base_diname'] =f"{base_diname:9.2f}"
            context['indemnisation_loyer'] = f"{indemnisation_ecart_loyer:9.2f}"
            context['prime_amg'] = f"{prime_amg:9.2f}"
            context['attractivite'] = attractivite
            context['moisMGES'] = moisMGES
            context['lbl_MGES'] = lbl_MGES
            context['prime_MGES'] = f"{prime_MGES:9.2f}"
            context['prime_MGEE'] = f"{prime_MGEE:9.2f}"
            context['total_diname'] = f"{total_diname:9.2f}"
            context['total_diname_an'] = f"{total_diname_an:9.2f}"
            context['total_general'] = f"{total_general:9.2f}"

    context["form"] = form

    return render(request, 'diname/diname.html/', context=context)

