from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('pedidos/', views.pedido, name='pedidos'),
    path('pagamentos/', views.view_that_asks_for_money, name='pagamento'),
    path('reverse/', views.paypal_reverse, name='paypal-reverse'),
    path('cancel/', views.paypal_cancel, name='paypal-cancel'),
]