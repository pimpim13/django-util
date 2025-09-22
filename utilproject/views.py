from django.http import HttpResponse
from django.shortcuts import render
#from utilproject.util import recup_ip


def home(request):
    #ip = recup_ip(request)
    return render(request, 'home.html', {"toto": "Accueil",
                                         "ip": "0.0.0.0" })

