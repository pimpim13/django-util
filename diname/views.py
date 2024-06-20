from django.shortcuts import render
from django.http import JsonResponse

from snb.models import Snb_ref_New, Coeff_New, Echelon
from diname.models import Site

from snb.api_snb import calcul_salaire_mensuel
from diname.forms import DinameForm

DATE = Snb_ref_New.objects.first().date_application


NR_PLANCHER = 130
NR_PLAFOND = 280
ECH_PLANCHER = 4
ECH_PLAFOND = 7
context = {}


def diname(request):

    context['attractivite'] = "bg-secondary"
    form = DinameForm()
    context["form"] = form

    return render(request, 'diname/diname.html/', context=context)


def recalcul(request):

    context = {}

    echelon = float(request.POST.get('echelon', 4.0))
    maj_res = float(request.POST.get('maj_res', 1.24))
    tps_trav = float(request.POST.get('tps_trav', 1.0))
    nr = request.POST.get('Nr', 30)

    snb1 = float(Snb_ref_New.objects.filter(date_application=DATE)[0].snb)

    coeff_nr1 = Coeff_New.objects.filter(date_application__lte=DATE, NR=nr)[0].valeur
    coeff_nr_plancher = Coeff_New.objects.filter(date_application__lte=DATE, NR=NR_PLANCHER)[0].valeur
    coeff_nr_plafond = Coeff_New.objects.filter(date_application__lte=DATE, NR=NR_PLAFOND)[0].valeur

    echelon_plancher = Echelon.objects.get(echelon=ECH_PLANCHER).coeff
    echelon_plafond = Echelon.objects.get(echelon=ECH_PLAFOND).coeff

    salaire1 = round(calcul_salaire_mensuel(coeff=coeff_nr1,
                                            ech=echelon,
                                            maj_res=maj_res,
                                            tps_trav=tps_trav,
                                            snb=snb1), 2)

    salaire_art30 = round(calcul_salaire_mensuel(coeff=coeff_nr1,
                                                 ech=echelon,
                                                 maj_res=maj_res,
                                                 tps_trav=1,
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

    limite50 = round(calcul_salaire_mensuel(coeff=coeff_nr1,
                                            ech=echelon,
                                            maj_res=maj_res,
                                            tps_trav=tps_trav,
                                            snb=snb1) * 13/2, 2)

    if request.POST.get('art30') == 'true':
        art30 = True
    else:
        art30 = False

    if request.POST.get('eligible_AMG') == 'true':
        eligible_AMG = True
    else:
        eligible_AMG = False

    if request.POST.get('eligible_MGEE') == 'true':
        eligible_MGEE = True
    else:
        eligible_MGEE = False

    if request.POST.get('agentGDP') == 'true':
        agentGDP = True
    else:
        agentGDP = False

    if request.POST.get('GDP_loge') == 'true':
        GDP_loge = True
    else:
        GDP_loge = False

    if request.POST.get('eligible_MR') == 'true':
        MR = True
    else:
        MR = False

    if request.POST.get('eligible_MGRa') == 'true':
        MGRa = True
    else:
        MGRa = False

    if request.POST.get('eligible_MGRb') == 'true':
        MGRb = True
    else:
        MGRb = False

    mois_MGRa = int(request.POST.get("mois_MGRa")) * MGRa
    mois_MGRb = int(request.POST.get("mois_MGRb")) * MGRb
    mois_MR = 1 * MR

    ind_art30 = round(salaire_art30 * 2, 2) * art30
    surface = request.POST.get('famille', 77)

    loyer_origine = Site.objects.get(localisation=request.POST.get('site_origine')).loyer
    loyer_destination = Site.objects.get(localisation=request.POST.get('site_destination')).loyer * int(not GDP_loge)
    ecart_loyer = round(max((loyer_destination - loyer_origine), 0), 2) 

    indemnisation_ecart_loyer = round(ecart_loyer * 12 * 5 * float(surface), 2) * eligible_AMG
    base_diname = min(max(plancher, salaire1), plafond)
    if not GDP_loge:
        prime_amg = base_diname * 5 * eligible_AMG
    else:
        prime_amg = float(0)

    loyer_origine_gdp = 0
    ecart_loyer_gdp = 0
    ecart_loyer_3 = 0

    if agentGDP:
        loyer_origine_gdp = round(min(salaire1 * 0.15, loyer_origine * float(surface)), 2)
        ecart_loyer_gdp = (loyer_destination * float(surface) - loyer_origine_gdp) * 12 * 2
        ecart_loyer_3 = max(((loyer_destination - loyer_origine) * float(surface) * 12 * 3), 0)
        indemnisation_ecart_loyer = (max(ecart_loyer_gdp, 0) + max(ecart_loyer_3, 0)) * eligible_AMG

    total_loyer_origine = round(loyer_origine * float(surface), 2)
    total_loyer_destination = round(loyer_destination * float(surface), 2)

    attractivite = Site.objects.get(localisation=request.POST.get('site_destination')).attractivite.couleur
    moisMGES = Site.objects.get(localisation=request.POST.get('site_destination')).attractivite.mois * int(not GDP_loge)
    lbl_MGES = Site.objects.get(localisation=request.POST.get('site_destination')).attractivite.lbl_MGES

    if GDP_loge:
        prime_MGES = float(0)
    else:
        prime_MGES = round(base_diname * moisMGES, 2) * eligible_AMG

    context['mois_MGEE'] = 0
    prime_MGEE = 0

    prime_MR = round(mois_MR * base_diname, 2) * MR
    prime_MGRa = round(mois_MGRa * base_diname, 2) * MGRa
    prime_MGRb = round(mois_MGRb * base_diname, 2) * MGRb

    if eligible_MGEE:
        if art30:
            prime_MGEE = round(base_diname * 2, 2)
            context['mois_MGEE'] = 2
        else:
            prime_MGEE = base_diname
            context['mois_MGEE'] = 1

    prime_reorg = prime_MR + prime_MGRa + prime_MGRb

    total_diname = round(min(prime_amg + prime_MGES + indemnisation_ecart_loyer, 100000) + prime_MGEE + prime_reorg, 2)
    total_diname_mobilite_geo = round(min(prime_amg + indemnisation_ecart_loyer + prime_MGES, 100000), 2)
    total_diname_mobilite_fonc = round(prime_MGEE, 2)
    total_diname_avant_ecretage = round((prime_amg + indemnisation_ecart_loyer + prime_MGES + prime_MGEE + prime_reorg), 2)
    total_diname_an = round(min(total_diname / 5, limite50), 2)

    total_general = total_diname + ind_art30

    context["salaire_mensuel"] = f"{salaire1:9.2f}"
    context["salaire_art30"] = f"{salaire_art30:9.2f}"
    context["mois_art30"] = 2 * art30
    context["art30"] = art30
    context['ind_art30'] = f"{ind_art30:9.2f}"
    context['surface'] = surface
    context['agentGDP'] = agentGDP
    context['GDP_loge'] = GDP_loge
    context["loyer_origine"] = f"{loyer_origine:9.2f}"
    context["loyer_origine_gdp"] = f"{loyer_origine_gdp:9.2f}"
    context["loyer_destination"] = f"{loyer_destination:9.2f}"
    context["total_loyer_origine"] = f"{total_loyer_origine:9.2f}"
    context["total_loyer_destination"] = f"{total_loyer_destination:9.2f}"
    context["ecart_loyer_gdp"] = f"{ecart_loyer_gdp:9.2f}"
    context["ecart_loyer_3"] = f"{ecart_loyer_3:9.2f}"
    context["ecart_loyer"] = f"{ecart_loyer:9.2f}"
    context["ecart_loyer_gdp"] = f"{ecart_loyer_gdp:9.2f}"
    context['plancher'] = f"{plancher:9.2f}"
    context['plafond'] = f"{plafond:9.2f}"
    context['base_diname'] = f"{base_diname:9.2f}"
    context['indemnisation_loyer'] = f"{indemnisation_ecart_loyer:9.2f}"
    context['prime_amg'] = f"{prime_amg:9.2f}"
    context['attractivite'] = attractivite
    context['moisMGES'] = moisMGES
    context['lbl_MGES'] = lbl_MGES
    context['prime_MGES'] = f"{prime_MGES:9.2f}"
    context['prime_MGEE'] = f"{prime_MGEE:9.2f}"
    context['mois_MR'] = mois_MR
    context['mois_MGRa'] = mois_MGRa
    context['mois_MGRb'] = mois_MGRb
    context['prime_MR'] = f"{prime_MR:9.2f}"
    context['prime_MGRa'] = f"{prime_MGRa:9.2f}"
    context['prime_MGRb'] = f"{prime_MGRb:9.2f}"
    context['prime_reorg'] = f"{prime_reorg:9.2f}"
    context['total_diname'] = f"{total_diname:9.2f}"
    context['total_diname_mobilite_geo'] = f"{total_diname_mobilite_geo:9.2f}"
    context['total_diname_mobilite_fonc'] = f"{total_diname_mobilite_fonc:9.2f}"
    context['total_diname_an'] = f"{total_diname_an:9.2f}"
    context['total_general'] = f"{total_general:9.2f}"
    context['total_diname_avant_ecretage'] = f"{total_diname_avant_ecretage:9.2f}"

    return JsonResponse(context)

