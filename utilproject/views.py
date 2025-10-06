from django.shortcuts import render


def home(request):
    #ip = recup_ip(request)
    return render(request, 'home.html', {"message": "Les frais 2025 vont bientôt être disponibles",
                                         "ip": "0.0.0.0" })

