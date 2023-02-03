from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class UserADM(UserAdmin):
    list_display = ("username", "is_staff", "email", "endereco", "cidade", "bairro", "estado", "cep")
    list_editable = ("email", "endereco", "cidade", "bairro","estado", "cep")

admin.site.register(User, UserADM)