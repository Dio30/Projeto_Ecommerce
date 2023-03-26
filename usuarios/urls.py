from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('cadastro/', UsuariosViews.as_view(), name='cadastrar'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('sair/', auth_views.LogoutView.as_view(), name='logout'),
    path('editar_perfil/<slug:slug>', UsuariosChangeView.as_view(), name='editar_perfil'),
    path('email_reset_senha/', EmailPasswordReset.as_view(), name='email_reset_senha'),
    path('email_reset_senha_enviado/', auth_views.PasswordResetDoneView.as_view(template_name="cadastro/email_reset_senha_enviado.html"), name='password_reset_done'),
    path('email_nova_senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="cadastro/email_nova_senha.html"), name='password_reset_confirm'),
    path('email_reset_senha_feito/', auth_views.PasswordResetCompleteView.as_view(template_name="cadastro/email_reset_senha_feito.html"), name='password_reset_complete'),
    ]