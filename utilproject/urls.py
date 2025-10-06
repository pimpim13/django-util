from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('pim/', include('pim.urls')),
    path('cet/', include('cet.urls')),
    path('frais/', include('frais.urls')),
    path('indemnites/', include('ind_dep.urls')),
    path('remuneration/', include('snb.urls')),
    path('diname/', include('diname.urls')),
    # path('accounts/profile/', profile, name='profile'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
#    path('testpdf/', pdf_display, name='pdf_display')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)