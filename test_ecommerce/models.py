from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    nome = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=200, null=True)
    preco = models.FloatField()
    imagem = models.ImageField(null=True, blank=True, upload_to='produtos', default='/s')
    digital = models.BooleanField(default=False, null=True, blank=False)
    
    def __str__(self):
        return self.nome
    
    @property 
    def image_url(self): # para poder visualizar fotos no html
        if self.imagem and hasattr(self.imagem, 'url'):
            return self.imagem.url
    
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    data_pedido = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False, verbose_name='Pedido Completado')
    id_transacao = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return f'Nº {self.id_transacao}'
    
    @property
    def envio(self):
        envio = False
        pedidoItem = self.pedidoitem_set.all()
        for i in pedidoItem:
            if i.produto.digital == False:
                envio = True
        return envio
    
    @property
    def pegar_carrinho_total(self):
        itens = self.pedidoitem_set.all()
        total = sum([item.pegar_total for item in itens])
        return total
    
    @property
    def pegar_carrinho_itens(self):
        itens = self.pedidoitem_set.all()
        total = sum([item.quantidade for item in itens])
        return total

class PedidoItem(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True, blank=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True, blank=True)
    quantidade = models.IntegerField(default=0, null=True, blank=True)
    data_adicao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(f'Item {self.produto} pedido nº {self.pedido}')
    
    @property
    def pegar_total(self):
        total = self.produto.preco * self.quantidade
        return total
    
class EnderecoEnvio(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True, blank=True)
    endereco = models.CharField(max_length=200, null=True)
    cidade = models.CharField(max_length=200, null=True)
    estado = models.CharField(max_length=200, null=True)
    cep = models.CharField(max_length=200, null=True)
    data_adicao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.endereco