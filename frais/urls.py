from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('bareme', views.frais, name='frais'),
    path('bareme/<str:an>/', views.frais_an, name='frais_an'),
    path('update/ursaff/', views.maj_ursaff, name='ursaff'),
    path('update/ursaff/<str:item>/', views.maj_ursaff_item, name='ursaff_item'),
    path('delete/ursaff/<str:item>/', views.del_ursaff_item, name='ursaff_del_item'),
    path('new/ursaff/', views.new_ursaff_item, name='ursaff_new_item'),
    path('new/bareme/', views.new_bareme_item, name='bareme_new_item'),
    path('delete/bareme/', views.del_bareme, name='bareme_del'),
    path('delete/bareme/<str:item>', views.del_bareme_item, name='bareme_del_item'),
]
