from django.urls import path
from cet import views

urlpatterns = [
    path('', views.index_cet, name='cet_index'),
    path('<str:choix>/', views.cet_choix, name='cet_choix'),

    # path('index/reset/', views.reset, name='reset'),
]