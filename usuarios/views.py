from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .forms import UsuariosForm, UserFormTransform, MyAuthenticationForm, PasswordReset
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, AuditEntry
from django.contrib.auth.views import LoginView
from .signals import user_login_password_failed
from .services import send_mail_to_user_reset_password
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import PasswordResetView

class UsuariosViews(SuccessMessageMixin, CreateView):
    template_name = 'cadastro/cadastrar.html'
    form_class = UsuariosForm
    success_message = "Usuário criado com sucesso"
    success_url = reverse_lazy('login')

class UsuariosChangeView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'cadastro/editar_perfil.html'
    form_class = UserFormTransform
    success_message = "Endereço editado com sucesso!"
    success_url = reverse_lazy('home')
    
    def get_object(self, queryset=None):
        self.object = get_object_or_404(User, slug=self.kwargs['slug'], username=self.request.user)
        return self.object

class MyLoginView(LoginView):
    template_name = 'cadastro/login.html'
    form_class = MyAuthenticationForm

    def form_invalid(self, form):
        username = form.data.get('username')

        if username:
            try:
                user = User.objects.get(username=username)

                for error in form.errors.as_data()['__all__']:
                    if error.code == 'max_attempt':
                        # Envia email para o usuário resetar a senha.
                        send_mail_to_user_reset_password(self.request, user)

            except User.DoesNotExist:
                pass
            else:
                # Dispara o signal quando o usuário existe, mas a senha está errada.
                user_login_password_failed.send(
                    sender=__name__,
                    request=self.request,
                    user=user
                )

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        user = form.get_user()

        # Autentica usuário
        auth_login(self.request, user)

        # Zera o AuditEntry
        AuditEntry.objects.filter(
            email=user.email,
            action='user_login_password_failed'
        ).delete()

        return HttpResponseRedirect(self.get_success_url())

class EmailPasswordReset(PasswordResetView):
    template_name= "cadastro/senha_reset.html"
    form_class = PasswordReset