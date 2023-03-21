from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('login', views.signin, name='loguser'),
    path('signup', views.signup, name='signup'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html')),

    # path('index/reset/', views.reset, name='reset'),
]