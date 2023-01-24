from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from paypal.standard.forms import PayPalPaymentsForm
import uuid
import json
import datetime
from .models import *

def home(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, complete=False)
        itens = pedido.pedidoitem_set.all()
        cart_itens = pedido.pegar_carrinho_itens
    else:
        itens = []
        pedido = {'pegar_carrinho_total':0, 'pegar_carrinho_itens':0, 'envio':False}
        cart_itens = pedido['pegar_carrinho_itens']
    produtos = Produto.objects.all()
    context = {'produtos':produtos, 'cart_itens':cart_itens}
    return render(request, 'compras/home.html', context)

def cart(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, complete=False)
        itens = pedido.pedidoitem_set.all()
        cart_itens = pedido.pegar_carrinho_itens
    else:
        itens = []
        pedido = {'pegar_carrinho_total':0, 'pegar_carrinho_itens':0, 'envio':False}
        cart_itens = pedido['pegar_carrinho_itens']
    context = {'itens':itens, 'pedido':pedido, 'cart_itens':cart_itens}
    return render(request, 'compras/cart.html', context)

def pedido(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, complete=False)
        itens = pedido.pedidoitem_set.all()
        cart_itens = pedido.pegar_carrinho_itens
    else:
        itens = []
        pedido = {'pegar_carrinho_total':0, 'pegar_carrinho_itens':0, 'envio':False}
        cart_itens = pedido['pegar_carrinho_itens']
    context = {'itens':itens, 'pedido':pedido, 'cart_itens':cart_itens}
    return render(request, 'compras/pedidos.html', context)

def updateItem(request):
    data = json.loads(request.body)
    produtoId = data['produtoId']
    action = data['action']
    cliente = request.user.cliente
    produto = Produto.objects.get(id=produtoId)
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, complete=False)
    pedidoItem, criado = PedidoItem.objects.get_or_create(pedido=pedido, produto=produto)
    if action == 'add':
        pedidoItem.quantidade = (pedidoItem.quantidade + 1)
    elif action == 'remove':
        pedidoItem.quantidade = (pedidoItem.quantidade - 1)
    pedidoItem.save()
    
    if pedidoItem.quantidade <= 0:
        pedidoItem.delete()
    return JsonResponse('Item foi adicionado com sucesso!', safe=False)

def processo_pedido(request):
    id_transacao = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        cliente = request.user.cliente
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, complete=False)
        total = float(data['form']['total'])
        pedido.id_transacao = id_transacao
        
        if total == float(pedido.pegar_carrinho_total):
            pedido.complete = True
        pedido.save()
        
        if pedido.envio == True:
            EnderecoEnvio.objects.create(
                cliente=cliente,
                pedido=pedido,
                endereco=data['envio']['address'],
                cidade=data['envio']['city'],
                estado=data['envio']['state'],
                cep=data['envio']['zipcode'],
                )
    return JsonResponse('Pagamento realizado!', safe=False)
    

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