from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from snb.views import SnbListView, SnbUpdate, compute, test

urlpatterns = [
    re_path(r'^$', views.snb, name='snb'),
    # re_path(r'^#result/$', views.snb, name='snb_result'),
    # path('update/snb/', views.snb_list, name='snb_list'),
    path('update/snb/', SnbListView.as_view(), name='snb_list'),
    # path('update/snb/<str:item>/', views.snb_update_item, name='snb_update_item'),
    path('update/snb/<int:pk>/', SnbUpdate.as_view(), name='snb_update_item'),
    path('delete/snb/<str:item>/', views.snb_delete_item, name='snb_delete_item'),
    path('new/snb/', views.snb_new, name='snb_new_item'),

    path('evolution/', views.snb_evol, name='snb_evol'),
    path('evolution/compute/', views.compute, name='compute'),

    path('transposition/', views.snb_transpose, name='snb_transposition'),
    path('transposition/compute/', views.transpose_compute, name='transpose_compute'),

    path('test/', views.test, name='test'),
]