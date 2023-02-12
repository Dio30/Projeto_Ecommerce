from django.contrib import admin
from .models import *

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco')

admin.site.register(Produto, ProdutoAdmin)

class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('endereco', 'cliente', 'data_adicao')
    search_fields = ('endereco',)

admin.site.register(EnderecoEnvio, EnderecoAdmin)

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id_transacao', 'complete', 'data_pedido')
    readonly_fields = ['id_transacao', 'complete']

admin.site.register(Pedido, PedidoAdmin)

class PedidoItemAdmin(admin.ModelAdmin):
    readonly_fields = ['produto', 'quantidade', 'pedido']
    list_display = ('pedido', 'quantidade', 'produto', 'pegar_total', 'data_adicao')
admin.site.register(PedidoItem, PedidoItemAdmin)