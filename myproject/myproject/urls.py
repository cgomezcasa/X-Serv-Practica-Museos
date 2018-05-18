from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'cargar$', 'museoApp.views.xmlParser'),
    url(r'^$', 'museoApp.views.pagina_principal'),
    url(r'^museos$', 'museoApp.views.museos'),
    url(r'^museo/(\d+)$', 'museoApp.views.museos_id'),
    url(r'^acceso$', 'museoApp.views.filtro_accesibilidad'),
    url(r'^distrito$', 'museoApp.views.filtro_distrito'),
    url(r'^(.*)','museoApp.views.notOption')
]
