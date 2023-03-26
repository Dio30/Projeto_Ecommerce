from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.core.validators import URLValidator

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) + text_type(user.email)
        )

account_activation_token = AccountActivationTokenGenerator()

def send_mail_to_user_reset_password(request, user):
    current_site = get_current_site(request)
    use_https = request.is_secure()
    subject = 'Aviso: Erro em tentativas de login.'
    message = render_to_string('cadastro/reset_de_senha.html', {
        'user': user,
        'protocol': 'https' if use_https else 'http',
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    user.email_user(subject, message)