from django.db import models

class Order(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(max_length=200)
    imagem = models.ImageField(blank=True, null=True)
