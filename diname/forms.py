from django import forms
from diname.models import Site, Famille, Emplois
from snb.models import Echelon, Coeff_New, Snb_ref_New
from datetime import date


class DinameForm(forms.Form):
    ART_30_CHOICE = [(True, True), (False, False)]
    SITES_CHOICE = [(a.localisation, a.localisation) for a in Site.objects.all()]
    FAMILLE_CHOICE = [(a.surface, a.situation) for a in Famille.objects.all()]
    NR_CHOICE = [(a.NR, a.NR) for a in Coeff_New.objects.filter(date_application=date(1900, 1, 1))]
    ECHELON_CHOICE = [(a.coeff, a.echelon) for a in Echelon.objects.filter(echelon__gt=3)]
    MAJ_RES_CHOICE = [(1.24, '24%'), (1.245, '24,5%'), (1.25, '25%')]
    TPS_TRAV_CHOICE = [(1, '35h ou CFJ'), (0.9714285714, '32h Coll.'), (0.9428571429, '32h Indiv.'), (0.707, "24h")]
    ETABLISSEMENT_CHOICE = [('EXPLOITATION', 'EXPLOITATION'),
                            ('FC', 'FC'),
                            ('MAINTENANCE', 'MAINTENANCE'),
                            ('DI', 'DI')]
    EMPLOI_CHOICE = [(a, a) for a in Emplois.objects.filter(actif=True)]

    Nr = forms.ChoiceField(label='Nr ', choices=NR_CHOICE, initial=180)
    echelon = forms.ChoiceField(label="Echelon actuel", choices=ECHELON_CHOICE, initial=1.22)
    maj_res = forms.ChoiceField(label='Maj rés', choices=MAJ_RES_CHOICE, initial=1.25)
    tps_trav = forms.ChoiceField(label='ATT', choices=TPS_TRAV_CHOICE)

    # art30 = forms.ChoiceField(label='article 30', widget=forms.CheckboxInput,
    #                           choices=ART_30_CHOICE, required=False)

    art30 = forms.BooleanField(label='article 30', required=False, initial=True)
    eligible_AMG = forms.BooleanField(label='Eligible AMG', required=False, initial=True)

    famille = forms.ChoiceField(label='Situation familiale', choices=FAMILLE_CHOICE, initial=FAMILLE_CHOICE[0][0])
    site_origine = forms.ChoiceField(label="Site Rte de départ", choices=SITES_CHOICE)
    site_destination = forms.ChoiceField(label="Site Rte d'arrivée", choices=SITES_CHOICE, initial=SITES_CHOICE[-1][-1])
    agentGDP = forms.BooleanField(label="Agent de GDP", required=False, initial=False)

    # etablissement = forms.ChoiceField(label='Etablissement', choices=ETABLISSEMENT_CHOICE, required=True)
    emploi = forms.ChoiceField(label="Emplois encouragés", choices=EMPLOI_CHOICE, required=False)

    eligible_MGEE = forms.BooleanField(label='Eligible MGEE', required=False, initial=False)


