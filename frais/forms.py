from pprint import pprint

from django import forms

from frais import parse_xl
from frais.models import ursaffModel

bareme_total = parse_xl.get_json('static/datas/2022.json')
ursaff = parse_xl.get_json('static/datas/ursaff.json')

localisations = sorted(bareme_total.keys())
loc = [(localisation, localisation) for localisation in localisations ]
annee = [(an, an) for an in ursaff.keys()]


CHOICES_COLLEGE = [('M', 'Execution/Maitrise'),
               ('C', 'Cadre'),
               ]

CHOICES_TAUX = [(0.0, '0%'),
                (11.0, '11%'),
                (30.0, '30%'),
                (41.0, '41%'),
                (45.0, '45%'),
                ]

CHOICES_MEMO = [(True, ""),
                (False, "")]

YEAR_CHOICES = [(a.annee, a.annee) for a in ursaffModel.objects.all()]


class FraisForm(forms.Form):

    # annee = forms.ChoiceField(label="Année", choices=YEAR_CHOICES)
    taux = forms.ChoiceField(label="Taux marginal impôt", choices=CHOICES_TAUX)
    localisation = forms.ChoiceField(label="Localisation", choices=loc)
    college = forms.ChoiceField(label='Collège', choices=CHOICES_COLLEGE)
    memo = forms.ChoiceField(label="Se souvenir de moi", widget=forms.CheckboxInput,
                             initial=True, choices=CHOICES_MEMO, required=False)

    class Meta:
        fields = ['taux', 'localisation', 'college', 'memo']


class updateUrsaffForm(forms.ModelForm):

    class Meta:
        model = ursaffModel
        fields = ['taux_cs', 'taux_cs_non_soumise']
        labels = {'taux_cs': 'Taux Ursaff', 'taux_cs_non_soumise': 'Taux Impôts'}

        # widgets = {'annee': forms.Select(choices=YEAR_CHOICES)}


class newUrsaffForm(forms.ModelForm):

    class Meta:
        model = ursaffModel
        fields = ['annee', 'taux_cs', 'taux_cs_non_soumise']
        labels = {'taux_cs': 'Taux Ursaff', 'taux_cs_non_soumise': 'Taux Impôts'}


if __name__ == '__main__':
    print('hello')


