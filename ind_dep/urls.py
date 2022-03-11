from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ind_dep, name='ind_dep'),
]
