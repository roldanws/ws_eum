from django.contrib import admin

# Register your models here.
from .models import Recurso,Contenido
# Register your models here.

class recursoAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)

class contenidoAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)


admin.site.register(Contenido,contenidoAdmin)

admin.site.register(Recurso,recursoAdmin)
