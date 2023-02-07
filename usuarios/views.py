from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .forms import UsuariosForm, UserFormTransform
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User

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