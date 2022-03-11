from django import forms


class DataForm(forms.Form):

    CHOICES = [(194, '5J / sem'),
               (184, '4J / sem'),
               (190, 'CFJ'),
               ]

    NBJOURTT = [(0, "0"),
                (1, "1"),
                (2, "2"),
                (3, "3"),
                ]

    CHOIXTC = [(True, 'Oui'),
               (False, 'Non'),
               ]

    aller_actuel_mn = forms.IntegerField(label='Durée trajet "Aller" actuel', max_value=240, min_value=0)
    aller_futur_mn = forms.IntegerField(label='Durée trajet "Aller" futur', max_value=240, min_value=0)
    retour_actuel_mn = forms.IntegerField(label='Durée trajet "Retour" actuel', max_value=240, min_value=0)
    retour_futur_mn = forms.IntegerField(label='Durée trajet "Retour" futur', max_value=240, min_value=0)
    aller_actuel_km = forms.IntegerField(label='Distance km "Aller" actuel', max_value=200, min_value=0)
    aller_futur_km = forms.IntegerField(label='Distance km "Aller" futur', max_value=200, min_value=0)
    retour_actuel_km = forms.IntegerField(label='Distance km "Retour" actuel', max_value=200, min_value=0)
    retour_futur_km = forms.IntegerField(label='Distance km "Retour" futur', max_value=200, min_value=0)
    duree_tx_future = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    residant_marseille = forms.ChoiceField(label="Résident Marseille", choices=CHOIXTC,
                                           widget=forms.RadioSelect, initial=True)

    teletravail_futur = forms.ChoiceField(label='Nombre de jours télétravaillés par semaine futur', choices=NBJOURTT)

