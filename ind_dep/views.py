from django.shortcuts import render
from .api_dep import Indemnite
# test = Indemnite({"h_debut": "8:00", "d_trajet": "35", "h_depart": "6:00", "h_fin": "17:00", "h_retour": "18:10"})

def ind_dep(request):

    embauche = request.GET.get('h_debut', '08:00')
    sortie = request.GET.get('h_fin', '17:00')
    duree = request.GET.get('duree', 30)
    depart = request.GET.get('h_depart', '08:00')
    retour = request.GET.get('h_retour', '17:00')

    resultat = Indemnite({'h_debut': embauche,
                          'h_fin': sortie,
                          'd_trajet': duree,
                          'h_depart': depart,
                          'h_retour': retour
                          }).compute()

    context = {'timeD': embauche,
               'timeR': sortie,
               'duree': duree,
               'depart': depart,
               'retour': retour,
               'resultat': resultat
               }

    return render(request, 'ind_dep/indemnites.html', context=context)
