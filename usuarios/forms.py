from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from .models import User, AuditEntry
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

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

class MyAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Email ou nome de usuário')

    error_messages = {
        'inactive': _("This account is inactive."),
        'invalid_username': _("Usuário ou email invalidos."),
        'invalid_password': _("Senha inválida."),
        'max_attempt': _(
            "Você atingiu o número máximo de tentativas. "
            "Estamos te enviando um e-mail."
        ),
    }
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password
            )
            if self.user_cache is None:
                self.check_authentication_error(username)
            else:
                self.confirm_login_allowed(self.user_cache)
            return self.cleaned_data
        
    def check_authentication_error(self, username):
        '''
        Verifica se foi erro de autenticação.
        '''
        
        User = get_user_model()
        try:
            user = User.objects.get(Q(email__iexact=username) | Q(username__iexact=username))
        except User.DoesNotExist:
            raise self.get_invalid_login_error()
        else:
            self.check_max_attempts(user)
            raise self.get_invalid_password_error()
        
    def get_invalid_login_error(self):
        '''
        Verifica se foi erro de login.
        '''
        return ValidationError(
            self.error_messages['invalid_username'],
            code='invalid_login',
            params={'username': self.username_field},
        )

    def check_max_attempts(self, user):
        '''
        Verifica o número de tentativas de login.
        '''
        max_attempts = AuditEntry.objects.filter(
            email=user.email,
            action='user_login_password_failed'
        ).count()
        
        if max_attempts > 2:
            # Envia email para o usuário resetar a senha.
            # Envia pela views.
            raise self.get_max_attempts_error()
        
    def get_max_attempts_error(self):
        '''
        Verifica se excedeu o número de tentativas de login.
        '''
        return ValidationError(
            self.error_messages['max_attempt'],
            code='max_attempt',
            params={'username': self.username_field},
        )

    def get_invalid_password_error(self):
        '''
        Verifica se foi erro de senha inválida.
        '''
        return ValidationError(
            self.error_messages['invalid_password'],
            code='invalid_password',
            params={'username': self.username_field},
        )

class PasswordReset(PasswordResetForm):
    email = forms.EmailField(max_length=100,
        widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email', 
                                       'autofocus':'on', 'spellcheck':'false'}),
    )
    
    def clean_email(self):
        """
        Se o email não existir no banco de dados
        """
        e_mail = self.cleaned_data['email']
        user = User.objects.filter(email=e_mail)
        if not user.exists():
            raise ValidationError("Esse email não está cadastrado.")
        return e_mail