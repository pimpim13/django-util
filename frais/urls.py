from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.frais, name='frais'),

    # path('index/reset/', views.reset, name='reset'),
]
