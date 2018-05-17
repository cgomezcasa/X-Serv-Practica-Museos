from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'cargar$', 'museoApp.views.xmlParser'),
    url(r'^$', 'museoApp.views.pagina_principal'),
    url(r'^filtro$', 'museoApp.views.filtro_accesibilidad'),
    url(r'^(.*)','museoApp.views.notOption')
]
