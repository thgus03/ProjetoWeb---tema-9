from django.shortcuts import render, get_object_or_404, redirect
from .carrinho import Carrinho
from shop.models import Produto, Pedido
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

def carrinho(request):
    carrinho = Carrinho(request)
    carrinho_produtos = carrinho.get_produtos
    quantidade = carrinho.get_quantidade
    total_carrinho = carrinho.carrinho_total()
    return render(request, 'carrinho.html', {"carrinho_produtos": carrinho_produtos, 'quantidade': quantidade, 'total_carrinho': total_carrinho})

def carrinho_adicionar(request):
    carrinho = Carrinho(request)
    if request.POST.get('action') == 'post':
        produto_id = int(request.POST.get('product_id'))
        produto_quantidade = int(request.POST.get('product_qty'))
        produto = get_object_or_404(Produto, id=produto_id)
        carrinho.adicionar(produto=produto, quantidade=produto_quantidade)

        quantidade_carrinho = carrinho.__len__()
        response = JsonResponse({'quantidade': quantidade_carrinho})
        #response = JsonResponse({'Nome do produto': produto.nome})
        return response

def carrinho_deletar(request):
    carrinho = Carrinho(request)
    if request.POST.get('action') == 'post':
        produto_id = int(request.POST.get('product_id'))
        carrinho.deletar(produto=produto_id)
        response = JsonResponse({'produto': produto_id})
        return response

def carrinho_atualizar(request):
    carrinho = Carrinho(request)
    if request.POST.get('action') == 'post':
        produto_id = int(request.POST.get('product_id'))
        produto_quantidade = int(request.POST.get('product_qty'))

        carrinho.atualizar(produto=produto_id, quantidade=produto_quantidade)

        response = JsonResponse({'quantidade':produto_quantidade})
        return response
    
@login_required
def finalizar_compra(request):
    carrinho = Carrinho(request)
    cliente = request.user.cliente

    for produto_id, quantidade in carrinho.carrinho.items():
        produto = Produto.objects.get(id=produto_id)
        Pedido.objects.create(
            cliente=cliente,
            produto=produto,
            quantidade=quantidade,
            status=True  
        )
    
    request.session['session_key'] = {}
    messages.success(request, "Compra realizada com sucesso!")
    return redirect('home')