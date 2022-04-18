from django import forms
from snb.models import Snb_ref, Coeff, Echelon


class SnbUpdateForm(forms.ModelForm):

    class Meta:
        model = Snb_ref
        fields = ['annee', 'snb']
        labels = {'annee': 'Année', 'snb': 'SNB'}


class CalculSalaireForm(forms.Form):

    YEAR_CHOICES = [(a.annee, a.annee) for a in Snb_ref.objects.all()]
    NR_CHOICE = [(a.NR, a.valeur) for a in Coeff.objects.all()]
    ECHELON_CHOICE = [(a.echelon, a.coeff) for a in Echelon.objects.all()]
    MAJ_RES_CHOICE = [('24%', 1.24), ('24,5%', 1.245), ('25%', 1.25)]
    TPS_TRAV_CHOICE = [('35h', 1), ('32h Coll.', 0.971), ('32h Indiv.', 0.943)]

    annee = forms.ChoiceField(label='Année', choices=YEAR_CHOICES)
    Nr = forms.ChoiceField(label='Nr', choices=NR_CHOICE)
    echelon = forms.ChoiceField(label="Echelon d'ancienneté", choices=ECHELON_CHOICE)
    maj_res = forms.ChoiceField(label='Maroration résidentielle', choices=MAJ_RES_CHOICE)
    tps_trav = forms.ChoiceField(label='Temps de travail', choices=TPS_TRAV_CHOICE)