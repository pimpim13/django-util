from email.policy import default

from django import forms


class DataForm(forms.Form):

    CHOICES = [(194, '5J / sem'),
               (184, '4J / sem'),
               (190, 'CFJ 190'),
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

    NB_JOURS_TT = [(108, "108 jours"),
                   (20, "20 jours"),
                   (10, "10 jours")]


    CHOIXTC = [(True, 'Oui'),
               (False, 'Non'),
               ]

    CHOICES_MEMO = [(True, ""), (False, "")]

    aller_actuel_mn = forms.IntegerField(label='Durée trajet "aller" actuel', max_value=240, min_value=0)
    aller_futur_mn = forms.IntegerField(label='Durée trajet "aller" futur', max_value=240, min_value=0)
    # aller_actuel_km = forms.IntegerField(label='Distance km actuel', max_value=200, min_value=0)
    # aller_futur_km = forms.IntegerField(label='Distance km futur', max_value=200, min_value=0)
    duree_tx_future = forms.ChoiceField(label="Votre aménagement temps de travail", choices=CHOICES)
    # duree_tx_future = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    eligible_tt = forms.BooleanField(label="Eligible au Télétravail ?", widget=forms.CheckboxInput, required=False, initial=True)
    nb_jours_tt = forms.ChoiceField(label="Plafond annuel théorique de télétravail", choices=NB_JOURS_TT, widget=forms.RadioSelect)
    # memo = forms.BooleanField(label="Se souvenir de moi", widget=forms.CheckboxInput,
    #                          initial=True, required=False)
    #
    #
    # print('valeur de memo : ', memo)


