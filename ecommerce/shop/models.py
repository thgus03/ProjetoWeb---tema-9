from django.db import models
from django.contrib.auth.models import User
import datetime

#Categoria dos produtos
class Categoria(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

#Clientes
class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    primeiro_nome = models.CharField(max_length=50)
    ultimo_nome = models.CharField(max_length=50)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    senha = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.primeiro_nome} {self.ultimo_nome}'

#Produtos
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, default=1)
    descricao = models.CharField(max_length=250, default='', blank=True, null=True)
    imagem = models.ImageField(upload_to='uploads/produto/')
    #Promoção
    promocao = models.BooleanField(default=False)
    preco_promocao = models.DecimalField(default=0, decimal_places=2, max_digits=6)

    def __str__(self):
        return self.nome

#Pedidos do cliente
class Pedido(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)
    endereco = models.CharField(max_length=100, default='', blank=True)
    telefone = models.CharField(max_length=20, default='', blank=True)
    data = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.cliente} - {self.produto} - {self.quantidade}'
        
class Review(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    avaliacao = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comentario = models.TextField(default='',blank=True)
    data = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('produto', 'cliente')

    def __str__(self):
        return f"{self.cliente} - {self.produto} - {self.avaliacao}"
