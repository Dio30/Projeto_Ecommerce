from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.contrib.auth.signals import user_logged_in, user_logged_out
from .signals import user_login_password_failed

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
        swappable = settings.AUTH_USER_MODEL
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        else:
            self.slug = slugify(self.username)
        return super().save(*args, **kwargs)

class AuditEntry(models.Model):
    action = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True)
    email = models.CharField(max_length=256, null=True)

    def __unicode__(self):
        return f'{self.action}-{self.email}-{self.ip}'

    def __str__(self):
        return f'{self.action}-{self.email}-{self.ip}'

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(
        action='user_logged_in',
        ip=ip,
        email=user.email
    )

@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(
        action='user_logged_out',
        ip=ip,
        email=user.email
    )

@receiver(user_login_password_failed)
def user_login_password_failed(sender, **kwargs):
    user = kwargs['user']
    AuditEntry.objects.create(
        action='user_login_password_failed',
        email=user.email
    )