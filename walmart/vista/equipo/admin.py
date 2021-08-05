from django.contrib import admin

# Register your models here.
from .models import Equipo,Tarifa
# Register your models here.

class equipoAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)

class tarifaAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)

admin.site.register(Equipo,equipoAdmin)
admin.site.register(Tarifa,tarifaAdmin)
