from django.shortcuts import render, redirect
from .forms import DataForm
from .api import Indemnisation
from django.http import HttpResponse, HttpResponseRedirect

# from pim.models import Aideitem


def index(request):
    reset = 1
    if reset != 0:
        data = {"aller_actuel_mn": 15, "aller_futur_mn": 50, "retour_actuel_mn": 15, "retour_futur_mn": 50,
                "aller_actuel_km": 0, "retour_actuel_km": 0, "aller_futur_km": 0, "retour_futur_km": 0,
                "duree_tx_future": 194, "eligible_tt": True, "nb_jours_tt": 108, 'memo': True}
    else:
        data = {}

    indemnisation = {}

    if request.method == 'POST':
        form = DataForm(request.POST)
        if form.is_valid():
            data["aller_actuel_mn"] = form.cleaned_data["aller_actuel_mn"]
            data["aller_futur_mn"] = form.cleaned_data["aller_futur_mn"]
            data["duree_tx_future"] = form.cleaned_data["duree_tx_future"]
            data["eligible_tt"] = form.cleaned_data["eligible_tt"]
            data["nb_jours_tt"] = form.cleaned_data["nb_jours_tt"]



            indemnisation = Indemnisation(data).compute()
            tt = {"indem_tps_tt_75": indemnisation["indem_tps_tt_75"],
                  "indem_tps_tt_50": indemnisation["indem_tps_tt_50"],
                  }
            del indemnisation["indem_tps_tt_75"]
            del indemnisation["indem_tps_tt_50"]

    else:
        form = DataForm(data)
        tt = {"indem_tt_tps_75": 0}


    context = {"dico": data,
               "form": form,
               "indemnisation": indemnisation,
               "tt": tt,
               }

    # return render(request, "pim/index.html", context)
    return render(request, "pim/index.html", context)


def reset(request):
    request.method = 'GET'
    return redirect('index')


def help_item(request, item=""):
    # choice = ["tps-travail", "ecart_tps", "indem_tps", "allong_km", "indem_km", "indem_tps_tt", "indem_km_tt"]
    url = f"pim/{item}.html"
    context = {'url': url}
    # t = Aideitem.objects.get(item=item)
    # print(t.description)
    return render(request, 'pim/help.html', context=context)
