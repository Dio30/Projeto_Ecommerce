from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from paypal.standard.forms import PayPalPaymentsForm
import uuid

def home(request):
    context = {}
    return render(request, 'compras/home.html', context)

def cart(request):
    context = {}
    return render(request, 'compras/cart.html', context)

def pedido(request):
    context = {}
    return render(request, 'compras/pedidos.html', context)

def view_that_asks_for_money(request):
    host = request.get_host()
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "20.00",
        "item_name": "Product 1",
        "currency_code": "BRL",
        "invoice": str(uuid.uuid4()),
        "notify_url": f"http://{host}{reverse('paypal-ipn')}",
        "return": f"http://{host}{reverse('paypal-reverse')}",
        "cancel_return": f"http://{host}{reverse('paypal-cancel')}",
        "custom": "premium_plan",
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "compras/pagamentos.html", context)

def paypal_reverse(request):
    messages.success(request, 'Seu pagamento foi aceito com sucesso.')
    return redirect('pagamento')

def paypal_cancel(request):
    messages.error(request, 'Seu pagamento foi recusado!')
    return redirect('pagamento')