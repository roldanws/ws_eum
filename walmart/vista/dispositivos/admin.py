from django.contrib import admin

# Register your models here.
from .models import Dispositivo
# Register your models here.

class dispositivosAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)


admin.site.register(Dispositivo,dispositivosAdmin)
