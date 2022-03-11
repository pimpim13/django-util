from pprint import pprint

from django import forms

from frais import parse_xl
#import parse_xl

bareme_total = parse_xl.get_json('static/datas/2021.json')


localisations = sorted(bareme_total.keys())
loc = [(localisation, localisation) for localisation in localisations ]


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


class FraisForm(forms.Form):

    taux = forms.ChoiceField(label="Taux marginal impôt", choices=CHOICES_TAUX)
    localisation = forms.ChoiceField(label="Localisation", choices=loc)
    college = forms.ChoiceField(label='Collège', choices=CHOICES_COLLEGE)
    memo = forms.ChoiceField(label="Se souvenir de moi", widget=forms.CheckboxInput,
                             initial=True, choices=CHOICES_MEMO, required=False)


if __name__ == '__main__':
    pprint(loc)


