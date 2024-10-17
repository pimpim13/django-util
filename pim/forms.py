from email.policy import default

from django import forms


class DataForm(forms.Form):

    CHOICES = [(194, '5J / sem'),
               (184, '4J / sem'),
               (190, 'CFJ'),
               (197, 'CFJ 197'),
               (203, 'CFJ 203'),
               (209, 'CFJ 209'),
               ]

    NBJOURTT = [(0, "0"),
                (1, "1"),
                (2, "2"),
                (3, "3"),
                ]

    ELIGIBLE_TT = [(True, 'Oui'),
                   (False, 'Non'),
               ]

    NB_JOURS_TT = [(108, "108 jours/an"),
                   (20, "20 jours/an"),
                   (10, "10 jours/an")]


    CHOIXTC = [(True, 'Oui'),
               (False, 'Non'),
               ]

    aller_actuel_mn = forms.IntegerField(label='Durée trajet actuel', max_value=240, min_value=0)
    aller_futur_mn = forms.IntegerField(label='Durée trajet futur', max_value=240, min_value=0)
    aller_actuel_km = forms.IntegerField(label='Distance km actuel', max_value=200, min_value=0)
    aller_futur_km = forms.IntegerField(label='Distance km futur', max_value=200, min_value=0)
    duree_tx_future = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    eligible_tt = forms.BooleanField(label="Eligible au Télétravail ?", widget=forms.CheckboxInput, required=False)
    nb_jours_tt = forms.ChoiceField(choices=NB_JOURS_TT, widget=forms.RadioSelect)


