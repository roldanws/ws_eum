from django.contrib import admin

# Register your models here.
from .models import Servidor
# Register your models here.

class servidoresAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)


admin.site.register(Servidor,servidoresAdmin)
