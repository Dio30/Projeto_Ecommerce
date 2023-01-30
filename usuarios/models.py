from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    endereco = models.CharField(max_length=100, help_text='Insira o seu endereço.', null=True, blank=True)
    cidade = models.CharField(max_length=100, help_text='Insira a sua cidade.', null=True, blank=True)
    estado = models.CharField(max_length=100, help_text='Insira o seu estado.', null=True, blank=True)
    cep = models.CharField(max_length=8, help_text='Insira o seu CEP, se voce sabe o seu cep pode inseri-lo aqui que o endereço será preenchido automaticamente.', null=True, blank=True)

    class Meta:
        verbose_name = ("Usuário")
        verbose_name_plural = ("Usuários")