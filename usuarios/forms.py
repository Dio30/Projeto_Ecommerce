from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UsuariosForm(UserCreationForm):
    email = forms.EmailField(required=False)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        
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