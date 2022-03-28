from django import forms
from frais.models import ursaffModel, Bareme

an = Bareme.objects.last().annee
bareme_actuel = Bareme.objects.filter(annee=an)
localisations = sorted({_.localisation for _ in bareme_actuel})
loc = [(localisation, localisation) for localisation in localisations]

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


class newUrsaffForm(forms.ModelForm):

    class Meta:
        model = ursaffModel
        fields = ['annee', 'taux_cs', 'taux_cs_non_soumise']
        labels = {'taux_cs': 'Taux Ursaff', 'taux_cs_non_soumise': 'Taux Impôts'}


# class newBaremeForm(forms.Form):
#
#     annee = forms.IntegerField()


if __name__ == '__main__':
    print('hello')