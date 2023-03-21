from django import forms
from snb.models import Echelon, Coeff_New, Snb_ref_New
from datetime import date


class SnbUpdateForm(forms.ModelForm):

    class Meta:
        model = Snb_ref_New
        fields = ['annee', 'snb', 'date_application']
        labels = {'annee': 'Année', 'snb': 'SNB', 'date_application': "Date d'application"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['annee'].disabled = True


class SnbCreateForm(forms.ModelForm):

    class Meta:
        # model = Snb_ref
        model = Snb_ref_New
        fields = ['annee', 'snb', 'date_application']
        labels = {'annee': 'Année', 'snb': 'SNB', 'date_application': "Date d'application"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['annee'].disabled = False


class CalculSalaireForm(forms.Form):

    ARTT32CO = float(32/35)

    # YEAR_CHOICES = [(a.annee, a.annee) for a in Snb_ref_New.objects.all()]
    YEAR_CHOICES = [(a.date_application, a.date_application) for a in Snb_ref_New.objects.all()]
    NR_CHOICE = [(a.NR, a.NR) for a in Coeff_New.objects.filter(date_application=date(1900, 1, 1))]
    ECHELON_CHOICE = [(a.coeff, a.echelon) for a in Echelon.objects.filter(echelon__gt=3)]
    MAJ_RES_CHOICE = [(1.24, '24%'), (1.245, '24,5%'), (1.25, '25%')]
    TPS_TRAV_CHOICE = [(1, '35h'), (0.9714285714, '32h Coll.'), (0.9428571429, '32h Indiv.'), (0.707, "24h")]
    CHOICES_MEMO = [(True, ""), (False, "")]

    date_application = forms.ChoiceField(label='Année', choices=YEAR_CHOICES, initial=YEAR_CHOICES[0][0])
    Nr = forms.ChoiceField(label='Nr actuel', choices=NR_CHOICE)
    echelon = forms.ChoiceField(label="Echelon actuel", choices=ECHELON_CHOICE)
    maj_res = forms.ChoiceField(label='Maj rés', choices=MAJ_RES_CHOICE)
    tps_trav = forms.ChoiceField(label='ATT', choices=TPS_TRAV_CHOICE)
    # Nr_futur = forms.ChoiceField(label='Nr futur', choices=NR_CHOICE)
    # echelon_futur = forms.ChoiceField(label="Ech futur", choices=ECHELON_CHOICE)
    memo = forms.ChoiceField(label="Se souvenir de moi", widget=forms.CheckboxInput,
                             initial=True, choices=CHOICES_MEMO, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['annee'].disabled = False


class EvolSnbForm(forms.Form):

    NR_CHOICE = [(a.NR, a.NR) for a in Coeff_New.objects.filter(date_application=date(1900, 1, 1))]
    ECHELON_CHOICE = [(a.coeff, a.echelon) for a in Echelon.objects.filter(echelon__gt=3)]
    MAJ_RES_CHOICE = [(1.24, '24%'), (1.245, '24,5%'), (1.25, '25%')]
    TPS_TRAV_CHOICE = [(1, '35h'), (0.9714285714, '32h Coll.'), (0.9428571429, '32h Indiv.'), (0.707, "24h")]

    Nr = forms.ChoiceField(label='Nr ', choices=NR_CHOICE)
    echelon = forms.ChoiceField(label="Echelon actuel", choices=ECHELON_CHOICE)
    maj_res = forms.ChoiceField(label='Maj rés', choices=MAJ_RES_CHOICE)
    tps_trav = forms.ChoiceField(label='ATT', choices=TPS_TRAV_CHOICE)
    toto = forms.BooleanField(widget=forms.HiddenInput, initial=True, required=False)  # champs caché pour selection de formulaire
