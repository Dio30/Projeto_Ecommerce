from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Tenta buscar o usuário usando o endereço de e-mail OU nome de usuário
            user = UserModel.objects.get(Q(email__iexact=username) | Q(username__iexact=username))
        except UserModel.DoesNotExist:
            return None

        # Verifica se a senha fornecida é correta
        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
