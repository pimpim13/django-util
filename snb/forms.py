from django import forms
from snb.models import Snb_ref, Coeff, Echelon


class SnbUpdateForm(forms.ModelForm):

    class Meta:
        model = Snb_ref
        fields = ['annee', 'snb']
        labels = {'annee': 'Année', 'snb': 'SNB'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['annee'].disabled = True


class SnbCreateForm(forms.ModelForm):

    class Meta:
        model = Snb_ref
        fields = ['annee', 'snb']
        labels = {'annee': 'Année', 'snb': 'SNB'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['annee'].disabled = False


class CalculSalaireForm(forms.Form):

    YEAR_CHOICES = [(a.annee, a.annee) for a in Snb_ref.objects.all()]
    NR_CHOICE = [(a.valeur, a.NR) for a in Coeff.objects.all()]
    ECHELON_CHOICE = [(a.coeff, a.echelon) for a in Echelon.objects.filter(echelon__gt=3)]
    MAJ_RES_CHOICE = [(1.24, '24%'), (1.245, '24,5%'), (1.25, '25%')]
    TPS_TRAV_CHOICE = [(1, '35h'), (0.971, '32h Coll.'), (0.943, '32h Indiv.'), (0.707, "24h"), (1.08, "CFJ 197"), (1.12, "CFJ 206"), (1.16, "CFJ 209")]
    CHOICES_MEMO = [(True, ""), (False, "")]

    annee = forms.ChoiceField(label='Année', choices=YEAR_CHOICES, initial=YEAR_CHOICES[0][0])
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
        self.fields['annee'].disabled = True


