from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from .views import MEEListView, MEEUpdate

urlpatterns = [
    path('', views.diname, name='diname'),
    path('recalcul/', views.recalcul, name='recalcul'),

    path('update/mee/', MEEListView.as_view(), name='mee_list'),
    path('update/mee/<int:pk>/', MEEUpdate.as_view(), name='mee_update_item'),
    path('delete/mee/<str:item>/', views.mee_delete_item, name='mee_delete_item'),
    path('new/snb/', views.mee_new, name='mee_new_item'),
]
