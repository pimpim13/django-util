"""utilproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import home
from accounts.views import profile
from testapp.views import pdf_display

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('pim/', include('pim.urls')),
    path('cet/', include('cet.urls')),
    path('frais/', include('frais.urls')),
    path('indemnites/', include('ind_dep.urls')),
    path('remuneration/', include('snb.urls')),
    # path('accounts/profile/', profile, name='profile'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('testpdf/', pdf_display, name='pdf_display')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)