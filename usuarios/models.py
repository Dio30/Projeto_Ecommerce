from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify

class User(AbstractUser):
    endereco = models.CharField(max_length=100, help_text='Insira o seu endereço.', null=True, blank=True)
    cidade = models.CharField(max_length=100, help_text='Insira a sua cidade.', null=True, blank=True)
    bairro = models.CharField(max_length=100, help_text='Insira o seu bairro.', null=True, blank=True)
    estado = models.CharField(max_length=100, help_text='Insira o seu estado.', null=True, blank=True)
    cep = models.CharField(max_length=8, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        verbose_name = ("Usuário")
        verbose_name_plural = ("Usuários")
        swappable = "AUTH_USER_MODEL"
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        else:
            self.slug = slugify(self.username)
        return super().save(*args, **kwargs)