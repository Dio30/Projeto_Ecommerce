from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, AuditEntry

class UserADM(UserAdmin):
    list_display = ("username", "is_staff", "email", "endereco", "cidade", "bairro", "estado", "cep")
    list_editable = ("email", "endereco", "cidade", "bairro","estado", "cep")

admin.site.register(User, UserADM)


class AuditEntryAdmin(admin.ModelAdmin):
    list_display = ('action', 'email', 'ip', 'data')
    list_filter = ('action',)
    readonly_fields = ('action', 'email', 'ip', 'data')
    
admin.site.register(AuditEntry, AuditEntryAdmin)