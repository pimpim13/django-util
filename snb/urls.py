from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from snb.views import SnbListView, SnbUpdate, compute, test

urlpatterns = [
    re_path(r'^$', views.snb, name='snb'),
    path('update/snb/', SnbListView.as_view(), name='snb_list'),
    path('update/snb/<int:pk>/', SnbUpdate.as_view(), name='snb_update_item'),
    path('delete/snb/<str:item>/', views.snb_delete_item, name='snb_delete_item'),
    path('new/snb/', views.snb_new, name='snb_new_item'),
    path('transposition/', views.snb_transpose, name='snb_transposition'),
    path('transposition/compute/', views.transpose_compute, name='transpose_compute'),

]