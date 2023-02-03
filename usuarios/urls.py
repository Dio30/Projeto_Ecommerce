from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('cadastro/', UsuariosViews.as_view(), name='cadastrar'),
    path('login/', auth_views.LoginView.as_view(template_name = 'cadastro/login.html'), name='login'),
    path('sair/', auth_views.LogoutView.as_view(), name='logout'),
    path('editar_perfil/<slug:slug>', UsuariosChangeView.as_view(), name='editar_perfil'),
    ]