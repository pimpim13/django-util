from django import forms
#from bootstrap_datepicker_plus.widgets import DatePickerInput


class DateToTimeForm(forms.Form):

    depart_administratif = forms.DateField(label="Date de départ administratif", initial="01/07/2024")
    depart_physique = forms.DateField(label='Date de départ Physique souhaitée', initial="30/06/2023")
    reliquat_ca = forms.DecimalField(label='Congés annuels restants', decimal_places=2, initial=0)
    reliquat_fl = forms.IntegerField(label='Reliquat Fêtes locales', initial=0)
    reliquat_anciennete = forms.DecimalField(label='Reliquat Ancienneté', decimal_places=2, initial=0)
    bonification_18j = forms.IntegerField(label='Bonification 18 jours', initial=18)
