from django.contrib import admin
from .models import *

admin.site.register(Produto)

class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('endereco', 'data_adicao')
    search_fields = ('endereco',)

admin.site.register(EnderecoEnvio, EnderecoAdmin)

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id_transacao', 'complete', 'cliente', 'data_pedido')
    readonly_fields = ['id_transacao', 'cliente', 'complete']

admin.site.register(Pedido, PedidoAdmin)

class PedidoItemAdmin(admin.ModelAdmin):
    readonly_fields = ['produto', 'quantidade', 'pedido']
    list_display = ('pedido', 'quantidade', 'produto')
admin.site.register(PedidoItem, PedidoItemAdmin)