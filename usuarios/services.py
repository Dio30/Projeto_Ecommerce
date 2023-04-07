from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

def send_mail_to_user_reset_password(request, user):
    current_site = get_current_site(request)
    use_https = request.is_secure()
    subject = 'Aviso: Erro em tentativas de login.'
    message = render_to_string('cadastro/reset_de_senha.html', {
        'user': user,
        'protocol': 'https' if use_https else 'http',
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': PasswordResetTokenGenerator().make_token(user),
    })
    user.email_user(subject, message)