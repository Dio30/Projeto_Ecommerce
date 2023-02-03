from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
import requests
from datetime import datetime
from .models import *

@login_required(redirect_field_name='cadastro/login.html')
def home(request):
    if request.user.is_authenticated:
        cliente = request.user
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

@login_required(redirect_field_name='cadastro/login.html')
def cart(request):
    if request.user.is_authenticated:
        cliente = request.user
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, complete=False)
        itens = pedido.pedidoitem_set.all()
        cart_itens = pedido.pegar_carrinho_itens
        
    else:
        itens = []
        pedido = {'pegar_carrinho_total':0, 'pegar_carrinho_itens':0, 'itens':itens,'envio':False}
        cart_itens = pedido['pegar_carrinho_itens']
    
    context = {'itens':itens, 'pedido':pedido, 'cart_itens':cart_itens}
    return render(request, 'compras/cart.html', context)

@login_required(redirect_field_name='cadastro/login.html')
def updateItem(request):
    data = json.loads(request.body)
    produtoId = data['produtoId']
    action = data['action']
    cliente = request.user
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

@login_required(redirect_field_name='cadastro/login.html')
def pedido(request):
    if request.user.is_authenticated:
        cliente = request.user
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, complete=False)
        itens = pedido.pedidoitem_set.all()
        cart_itens = pedido.pegar_carrinho_itens
        
    else:
        itens = []
        pedido = {'pegar_carrinho_total':0, 'pegar_carrinho_itens':0, 'envio':False}
        cart_itens = pedido['pegar_carrinho_itens']
        
    context = {'itens':itens, 'pedido':pedido, 'cart_itens':cart_itens}
    return render(request, 'compras/pedidos.html', context)

@login_required(redirect_field_name='cadastro/login.html')
def processo_pedido(request):
    id_transacao = datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        cliente = request.user
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, complete=False)
        pedido.id_transacao = id_transacao
        total = float(data['form']['total'])
        carrinho = float(pedido.pegar_carrinho_total)
    
        if total == carrinho:
            pedido.complete = True
            pedido.save()
       
        if pedido.envio == True:
            EnderecoEnvio.objects.create(
                cliente=cliente,
                pedido=pedido,
                endereco=data['envio']['address'],
                cidade=data['envio']['city'],
                bairro=data['envio']['district'],
                estado=data['envio']['state'],
                cep=data['envio']['zipcode'],
                )
    return JsonResponse('Pagamento Aceito!', safe=False)