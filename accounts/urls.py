from django.urls import path
from . import views

urlpatterns = [
    # path('login', views.signin, name='loguser'),
    path('signup', views.signup, name='signup'),

    # path('index/reset/', views.reset, name='reset'),
]