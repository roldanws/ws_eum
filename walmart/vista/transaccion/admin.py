from django.contrib import admin

# Register your models here.
from .models import Transaccion
# Register your models here.

class transaccionAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)


admin.site.register(Transaccion,transaccionAdmin)
