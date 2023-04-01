from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('', views.diname, name='diname'),
    path('recalcul/', views.recalcul, name='recalcul')
]
