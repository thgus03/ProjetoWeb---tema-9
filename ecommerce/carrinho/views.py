from django.shortcuts import render, get_object_or_404
from .carrinho import Carrinho
from shop.models import Produto
from django.http import JsonResponse

def carrinho(request):
    carrinho = Carrinho(request)
    carrinho_produtos = carrinho.get_produtos
    return render(request, 'carrinho.html', {"carrinho_produtos": carrinho_produtos})

def carrinho_adicionar(request):
    carrinho = Carrinho(request)
    if request.POST.get('action') == 'post':
        produto_id = int(request.POST.get('product_id'))
        produto = get_object_or_404(Produto, id=produto_id)
        carrinho.adicionar(produto=produto)

        quantidade_carrinho = carrinho.__len__()
        response = JsonResponse({'quantidade': quantidade_carrinho})
        #response = JsonResponse({'Nome do produto': produto.nome})
        return response

def carrinho_deletar(request):
    pass

def carrinho_atualizar(request):
    pass
