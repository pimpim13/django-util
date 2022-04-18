
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from pathlib import Path
from utilproject.settings import MEDIA_ROOT
from snb.models import Snb_ref, Coeff
from snb.forms import SnbUpdateForm
from frais.parse_xl import populate_nr


def snb(request):

    if not Coeff.objects.all():
        populate_db_nr()

    return render(request, 'snb/snb.html')


def snb_list(request):
    context = {}
    list_snb = Snb_ref.objects.all()
    context['list_snb'] = list_snb
    context['maj'] = False

    return render(request, 'snb/snb_update.html', context=context)


def snb_update_item(request, item):

    context = {'an': item}
    success = False
    list_snb = Snb_ref.objects.all()
    context['list_snb'] = list_snb

    snb_an = Snb_ref.objects.get(annee=item)

    form = SnbUpdateForm(initial={'annee': item,
                                  'snb': snb_an.snb})

    if request.method == 'POST':

        form = SnbUpdateForm(request.POST)
        form.annee = snb_an.annee

        if form.is_valid():
            snb_an.snb = form.cleaned_data['snb']

            print(snb_an.snb)
            snb_an.save()
            context['maj'] = False
            return redirect('snb_list')
        # else:
        #     success = False

    context['success'] = success
    context['form'] = form
    context['maj'] = True
    context['new'] = False

    # return render(request, 'frais/ursaff_new.html', context=context)
    return render(request, 'snb/snb_update.html', context=context)


def snb_new(request):

    context = {}

    list_snb = Snb_ref.objects.all()
    context['list_snb'] = list_snb

    form = SnbUpdateForm()

    if request.method == 'POST':
        form = SnbUpdateForm(request.POST)

    if form.is_valid():
        form.save()
        success = True
        return redirect('snb_list')
    else:
        success = False

    context['success'] = success
    context['form'] = form
    context['maj'] = True
    context['new'] = True

    # return render(request, 'frais/ursaff_new.html', context=context)
    return render(request, 'snb/snb_update.html', context=context)


def snb_delete_item(request, item):
    Snb_ref.objects.get(annee=item).delete()
    return redirect('snb_list')


def populate_db_nr():
    datas = populate_nr()
    for data in datas:
        Coeff.objects.create(**data)
