from django.urls import path
from . import views

urlpatterns = [
    path('', views.carrinho, name="carrinho"),
    path('adicionar/', views.carrinho_adicionar, name="carrinho_adicionar"),
    path('deletar/', views.carrinho_deletar, name="carrinho_deletar"),
    path('atualizar/', views.carrinho_atualizar, name="carrinho_atualizar"),
]
