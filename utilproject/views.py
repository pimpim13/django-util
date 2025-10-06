from django.shortcuts import render


def home(request):
    #ip = recup_ip(request)
    return render(request, 'home.html', {"bandeau": "Les frais 2025 ont été mis à jour",
                                         "ip": "0.0.0.0" })

