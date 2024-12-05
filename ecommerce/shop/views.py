from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto, Pedido, Review, Cliente
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django import forms

def produto(request, id):
    produto = Produto.objects.get(id=id)
    reviews = Review.objects.filter(produto=produto)
    soma_avaliacao = sum([review.avaliacao for review in reviews])
    num_avaliacao = reviews.count()
    media_avaliacao = soma_avaliacao / num_avaliacao if num_avaliacao > 0 else 0
    return render(request, 'produto.html', {'produto':produto, 'reviews': reviews, 'media_avaliacao': media_avaliacao})

def home(request):
    produtos = Produto.objects.all()
    return render(request, 'home.html', {'produtos':produtos})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        nome_usuario = request.POST['nome_usuario']
        senha = request.POST['senha']
        usuario = authenticate(request, username=nome_usuario, password=senha)
        if usuario is not None:
            login(request, usuario)
            
            try:
                cliente = Cliente.objects.get(user=usuario)
            except Cliente.DoesNotExist:
                cliente = None  
            
            messages.success(request, "Você entrou!")
            return redirect('home')
        else:
            messages.error(request, "Erro, tente novamente.")
            return redirect('home')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("Você foi deslogado"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            primeiro_nome = form.cleaned_data['first_name']
            ultimo_nome = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            senha = form.cleaned_data['password1']
            
            cliente = Cliente.objects.create(
                user=usuario,  
                primeiro_nome=primeiro_nome,
                ultimo_nome=ultimo_nome,
                telefone='',  
                email=email,
                senha=senha
            )

            login(request, usuario)
            messages.success(request, "Você foi registrado com sucesso!")
            return redirect('home')
        else:
            messages.error(request, "Erro ao se registrar, tente novamente.")
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})
        
@login_required
def profile(request):
    cliente = request.user.cliente
    pedidos = Pedido.objects.filter(cliente=cliente, status=True)
    return render(request, 'profile.html', {'pedidos': pedidos})


@login_required
def adicionar_review(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    cliente = request.user.cliente

    if not Pedido.objects.filter(cliente=cliente, produto=produto, status=True).exists():
        messages.error(request, "Você só pode avaliar produtos que comprou.")
        return redirect('profile')

    if request.method == "POST":
        avaliacao = request.POST.get("avaliacao")
        comentario = request.POST.get("comentario")

        if not avaliacao:
            messages.error(request, "Por favor, selecione uma nota.")
            return redirect('adicionar_review', produto_id=produto.id)

        review, created = Review.objects.update_or_create(
            produto=produto,
            cliente=cliente,
            defaults={"avaliacao": avaliacao, "comentario": comentario}
        )

        if created:
            messages.success(request, "Sua avaliação foi criada com sucesso!")
        else:
            messages.success(request, "Sua avaliação foi atualizada com sucesso!")

        return redirect('profile')

    return render(request, 'review.html', {'produto': produto})

