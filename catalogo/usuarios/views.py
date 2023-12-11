from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from usuarios.forms import LoginForms, RegisterForms

@login_required
def index(request):
    user = User.objects.all()
    register_form = RegisterForms()
    login_form = LoginForms()
    return render(request, 'jogos/index.html', {'users': user, 'register_form': register_form, 'user_form': login_form})

@login_required
def dashboard(request):
    return render(request, "dashboard/dashboard.html")

def login(request):  # Renomeie esta função
    user_form = LoginForms()

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

    return render(request, 'jogos/index.html', {'user_form': user_form})


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
