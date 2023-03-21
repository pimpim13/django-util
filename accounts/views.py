from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from accounts.models import CustomUser


class CustomSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        # fields = UserCreationForm.Meta.fields
        fields = ("username", "email")


def signup(request):
    context = {}
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            context['errors'] = form.errors

    form = CustomSignupForm()
    context['form'] = form

    return render(request, 'registration/signup.html', context=context)


def profile(request):
    return redirect('home')