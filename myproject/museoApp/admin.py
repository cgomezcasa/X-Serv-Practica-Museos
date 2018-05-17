from django.contrib import admin

# Register your models here.

from museoApp.models import Museo
from museoApp.models import Content_User
from museoApp.models import Comentario
from museoApp.models import Configuracion

admin.site.register(Museo)
admin.site.register(Content_User)
admin.site.register(Comentario)
admin.site.register(Configuracion)
