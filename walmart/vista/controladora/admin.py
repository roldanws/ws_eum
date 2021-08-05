from django.contrib import admin

# Register your models here.
from .models import Controladora
# Register your models here.

class controladoraAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)


admin.site.register(Controladora,controladoraAdmin)
