from django.shortcuts import render, redirect, get_object_or_404
from .models import Jogo
from .forms import JogoForm
from django.core.paginator import Paginator, EmptyPage

# Create your views here.

def index(request):
    produtos = Jogo.objects.all()
    
    # Se houver um termo de pesquisa na solicitação GET
    search_term = request.GET.get('search', '')
    
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

    return render(request, 'jogos/index.html', {'produtos': produtos_paginados })

# CRUD

def adicionar_produto(request):
    if request.method == 'POST':
        form = JogoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('jogos/listar_produtos')
    else:
        form = JogoForm()
    return render(request, 'adicionar_produto.html', {'form': form})

#Deletar produtos
def delete_produto(request, produto_id):
    produto = Jogo.objects.get(id=produto_id)
    produto.delete()
    return redirect('jogos/listar_produtos')

def listar_produtos(request):
    # Obtém o parâmetro de ID da solicitação GET
    produto_id = request.GET.get('id')

    # Se um ID foi fornecido, filtra o produto pelo ID
    if produto_id:
        produto = get_object_or_404(Jogo, id=produto_id)
        # Retorna apenas o produto específico
        return render(request, 'jogos/listar_produtos.html', {'produto': produto, 'quantidade_produtos': Jogo.objects.count()})
    else:
 # Se nenhum ID foi fornecido, lista todos os produtos
        produtos = Jogo.objects.all()
        return render(request, 'jogos/listar_produtos.html', {'produtos': produtos, 'quantidade_produtos': Jogo.objects.count()})