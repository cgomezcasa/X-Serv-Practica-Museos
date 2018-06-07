from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login
#from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'cargar$', 'museoApp.views.xmlParser'),
    url(r'^$', 'museoApp.views.pagina_principal'),
    url(r'^museos$', 'museoApp.views.museos'),
    url(r'^museos/(\d+)$', 'museoApp.views.museos_id'),
    url(r'^acceso$', 'museoApp.views.filtro_accesibilidad'),
    url(r'^distrito$', 'museoApp.views.distrito'),
    url(r'^distrito/(.*)', 'museoApp.views.distrito_concreto'),
    url(r'^comentario_nuevo$', 'museoApp.views.comentar'),
    url(r'^titulo_nuevo$', 'museoApp.views.tituloUser'),
    url(r'^json/(.*)', 'museoApp.views.user_json'),
    url(r'^xml/(.*)', 'museoApp.views.user_xml'),
    url(r'^about$', 'museoApp.views.about'),
    url(r'^logout$', 'museoApp.views.mylogout'),
    url(r'^login$', 'museoApp.views.mylogin'),
    url(r'^(.*)', 'museoApp.views.user'),
]
