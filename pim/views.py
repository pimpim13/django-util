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
                "duree_tx_future": 194, "eligible_tt": False, "nb_jours_tt": 108}
    else:
        data = {}

    indemnisation = {}

    if request.method == 'POST':
        form = DataForm(request.POST)
        if form.is_valid():
            data["aller_actuel_mn"] = form.cleaned_data["aller_actuel_mn"]
            data["aller_futur_mn"] = form.cleaned_data["aller_futur_mn"]
            data["aller_actuel_km"] = form.cleaned_data["aller_actuel_km"]
            data["aller_futur_km"] = form.cleaned_data["aller_futur_km"]
            data["duree_tx_future"] = form.cleaned_data["duree_tx_future"]
            data["eligible_tt"] = form.cleaned_data["eligible_tt"]
            data["nb_jours_tt"] = form.cleaned_data["nb_jours_tt"]



            indemnisation = Indemnisation(data).compute()
            tt = {"indem_tps_tt": indemnisation["indem_tps_tt"],
                  "indem_km_tt": indemnisation["indem_km_tt"],
                  }
            del indemnisation["indem_tps_tt"]
            del indemnisation["indem_km_tt"]

        # else:
        #     tt = {"indem_tt_tps": 0, "indem_tt_km": 0, }


    else:
        form = DataForm(data)
        tt = {"indem_tt_tps": 0, "indem_tt_km": 0, }

        # tt = {"tt_tps": None, "tt_km": None, }

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
