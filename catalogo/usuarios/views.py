from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from jogos.models import Jogo
from jogos.forms import JogoForm
from django.core.paginator import Paginator, EmptyPage
from usuarios.forms import LoginForms, RegisterForms

@login_required
def index(request):
    user = User.objects.all()
    register_form = RegisterForms()
    login_form = LoginForms()
    # Criar uma instância do formulário JogoForm
    jogo_form = JogoForm()

    # Obter todos os produtos
    produtos = Jogo.objects.all()

    # Filtrar por termo de pesquisa, se fornecido
    search_term = request.GET.get('search', '')
    
    if search_term:
        produtos = Jogo.objects.filter(nome__icontains=search_term)
    else:
        produtos = Jogo.objects.all()

    # Número de itens por página
    items_por_pagina = 8

    # Obter o número da página a partir dos parâmetros da solicitação
    page = request.GET.get('page', 1)

    # Criar um objeto Paginator
    paginator = Paginator(produtos, items_por_pagina)

    try:
        produtos_paginados = paginator.page(page)
    except EmptyPage:
        # Se a página solicitada estiver fora do intervalo, exibir a última página disponível
        produtos_paginados = paginator.page(paginator.num_pages)

    return render(request, 'jogos/index.html', {'users': user, 'register_form': register_form, 'user_form': login_form, 'form': jogo_form, 'produtos_paginados': produtos_paginados, 'search_term': search_term})

@login_required
def dashboard(request):
    return render(request, "dashboard/dashboard.html")

def login(request):  # Renomeie esta função
    user_form = LoginForms()
    produtos = Jogo.objects.all()
    # Criar uma instância do formulário JogoForm
    jogo_form = JogoForm()
    
    # Se houver um termo de pesquisa na solicitação GET
    search_term = request.GET.get('search', '')
    
    if search_term:
        produtos = Jogo.objects.filter(nome__icontains=search_term)
    else:
        produtos = Jogo.objects.all()
    
    # Se houver um termo de pesquisa, filtra os produtos
    if search_term:
        produtos = Jogo.objects.filter(nome__icontains=search_term)
    else:
        produtos = Jogo.objects.all()

    # Número de itens por página
    items_por_pagina = 8  # Altere conforme necessário

    # Obtém o número da página a partir dos parâmetros da solicitação
    page = request.GET.get('page', 1)

    # Cria um objeto Paginator
    paginator = Paginator(produtos, items_por_pagina)

    try:
        produtos_paginados = paginator.page(page)
    except EmptyPage:
        # Se a página solicitada estiver fora do intervalo, exibe a última página disponível
        produtos_paginados = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        user_form = LoginForms(request.POST)

    if user_form.is_valid():
        email = user_form['email'].value()
        senha = user_form['senha'].value()
        user_temp = User.objects.get(email=email)

        usuario = auth.authenticate(
            request,
            username=user_temp.username,
            password=senha
        )

        if usuario is not None:
            auth.login(request, usuario)
            messages.success(request, 'Foi logado com sucesso!')
            if usuario.is_staff:
                return redirect('dashboard')
            else:
                return redirect('index')
        else:
            messages.error(request, 'Erro ao efetuar login')
            return redirect('index')

    return render(request, 'jogos/index.html', {'user_form': user_form, 'produtos':produtos_paginados, 'form': jogo_form, 'search_term': search_term})


@login_required
def register(request):
    if request.method == 'POST':
        form = RegisterForms(request.POST)

        if form.is_valid():
            name = form['name'].value()
            email = form['email'].value()
            password = form['password'].value()

            if User.objects.filter(username=name).exists():
                messages.error(request, 'Usuário já existente')
                return redirect('users')

            usuario = User.objects.create_user(
                username=name,
                email=email,
                password=password
            )
            usuario.save()
            messages.success(request, 'Usuario cadastrado com sucesso!')
            return redirect('users')

@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout efetuado com sucesso!')
    return redirect('login')

@login_required
def inative(request, id):
    user = User.objects.get(id=id)
    user.is_active = False
    user.save()
    messages.success(request, 'Usuario inativado com sucesso!')
    return redirect('users')

@login_required
def active(request, id):
    user = User.objects.get(id=id)
    user.is_active = True
    user.save()
    messages.success(request, 'Usuario ativado com sucesso!')
    return redirect('users')
