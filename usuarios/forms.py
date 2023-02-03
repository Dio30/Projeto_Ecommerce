from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.core.exceptions import ValidationError

class UsuariosForm(UserCreationForm):
    email = forms.EmailField(required=True)
    cep = forms.IntegerField(help_text='Se voce sabe o seu CEP pode inseri-lo aqui que o endereço será preenchido automaticamente.')
    
    class Meta:
        model = User
        fields = ["username", "email", "endereco", "cidade", "bairro", "estado", "cep", "password1", "password2"]
        
    def clean_username(self):
        u = self.cleaned_data['username']
        user = User.objects.filter(username=u)
        if user.exists():
            raise ValidationError(f'O usuário {u} já existe.')
        
        if u.isnumeric():
            raise ValidationError('O usuário não pode ser somente numérico.')
        return u
    
    def clean_email(self):
        e = self.cleaned_data['email']
        email = User.objects.filter(email=e).exclude(email='')
        if email.exists():
            raise ValidationError(f'O email {e} já existe.')
        return e

class UserFormTransform(UserChangeForm):
    email = forms.EmailField(required=True)
    cep = forms.IntegerField(help_text='Se voce sabe o seu CEP pode inseri-lo aqui que o endereço será preenchido automaticamente.')
    class Meta:
        model = User
        fields = ["username", "email", "endereco", "cidade", "bairro", "estado", "cep"]
        
    def clean_username(self):
        u = self.cleaned_data['username']
        user = User.objects.filter(username=u).exclude(id=self.instance.id)
        if u.isnumeric():
            raise ValidationError('O usuário não pode ser somente numérico!')
        if user.exists():
            raise ValidationError(f'O usuário {u} já existe!')
        return u
    
    def clean_email(self):
        e = self.cleaned_data['email']
        email = User.objects.filter(email=e).exclude(id=self.instance.id).exclude(email='')
        if email.exists():
            raise ValidationError(f'O email {e} já existe!')
        return e