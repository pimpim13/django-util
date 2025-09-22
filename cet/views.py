from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import DateToTimeForm
from .api_heures import CetToDate, DateToCet


# Create your views here.


def index_cet(request):

    return render(request, 'cet/cet.html', {"choix": "bien arrivé sur la page CET", })


# @login_required
def cet_choix(request, choix="timedate"):

    if choix == "timetodate":
        dico = {}
        form = DateToTimeForm()

        context = {"form": form}
        if request.method == 'POST':
            form = DateToTimeForm(request.POST)
            if form.is_valid():
                dico["end_date"] = (form.cleaned_data["depart_administratif"])
                dico["start_date"] = form.cleaned_data["depart_physique"]
                dico["reliquat_ca"] = form.cleaned_data["reliquat_ca"]
                dico["reliquat_fl"] = form.cleaned_data["reliquat_fl"]
                dico["bonif_jours"] = form.cleaned_data["bonification_18j"]
                dico["reliquat_anciennete"] = form.cleaned_data["reliquat_anciennete"]

                calcul = DateToCet(dico=dico).compute()

                context = {"form": form,
                           "calcul": calcul,
                           }

        return render(request, 'cet/cet_time.html', context)


    else:
        context = {"choix": "mauvais choix"}

    return render(request, 'cet/cet_time.html', context)

