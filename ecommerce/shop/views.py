from django.shortcuts import render, redirect
from .models import Produto
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms

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
            messages.success(request, ("Você entrou"))
            return redirect('home')
        else:
            messages.success(request, ("Erro, tente novamente"))
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
                form.save()
                nome_usuario = form.cleaned_data['username']
                senha = form.cleaned_data['password1']
                usuario = authenticate(username=nome_usuario, password=senha)
                login(request, usuario)
                messages.success(request, ("Você foi registrado com sucesso!"))
                return redirect('home')
            else:
                messages.success(request, ("Erro ao se registrar, tente novamente"))
                return redirect('register')
        else:
            return render(request, 'register.html', {'form':form})