from django.urls import path
from pim import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reset/', views.reset, name='reset'),
    path('help/<str:item>/', views.help_item, name='help'),

    # path('index/reset/', views.reset, name='reset'),
]
