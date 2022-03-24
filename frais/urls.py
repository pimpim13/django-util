from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.frais, name='frais'),
    path('ursaff/', views.maj_ursaff, name='ursaff'),
    path('ursaff/<str:item>/', views.maj_ursaff_item, name='ursaff_item'),

]
