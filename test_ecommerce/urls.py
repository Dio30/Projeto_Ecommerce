from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('pedidos/', views.pedido, name='pedidos'),
    path('update_item/', views.updateItem, name='update_item'),
    path('processo_pedido/', views.processo_pedido, name='processo_pedido'),
]