from django.shortcuts import render
from django.urls import reverse_lazy
import requests
from .forms import UsuariosForm
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin

class UsuariosViews(SuccessMessageMixin, CreateView):
    template_name = 'cadastro/cadastrar.html'
    form_class = UsuariosForm
    success_message = "Usuário criado com sucesso"
    success_url = reverse_lazy('login')