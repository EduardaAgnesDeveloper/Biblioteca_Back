from django.shortcuts import redirect, render
from django.http import HttpResponse
from usuarios.models import Usuario
from .models import Emprestimos, Livros, Categoria
from .forms import CadastroLivro, CategoriaLivro
from django.db.models import Q
from datetime import datetime

# Página inicial que exibe todos os livros
def home(request):
    if request.session.get('usuario'):
        usuario = Usuario.objects.get(id=request.session['usuario'])
        livros = Livros.objects.filter(usuario=usuario)
        total_livros = livros.count()
        form = CadastroLivro()
        form.fields['usuario'].initial = request.session['usuario']
        form.fields['categoria'].queryset = Categoria.objects.filter(usuario=usuario)

        content = {
            'livros': livros,
            'usuario_logado': request.session['usuario'],
            'form': form,
            'total_livro': total_livros,
        }
        return render(request, 'home.html', content)
    return redirect('/auth/login/?status=2')


# Ver um livro específico
def ver_livros(request, id):
    if request.session.get('usuario'):
        livro = Livros.objects.get(id=id)
        if request.session.get('usuario') == livro.usuario.id:
            usuario = Usuario.objects.get(id=request.session['usuario'])
            categoria_livro = Categoria.objects.filter(usuario=usuario)
            emprestimos = Emprestimos.objects.filter(livro=livro)
            content = {
                'livro': livro,
                'categoria_livro': categoria_livro,
                'emprestimos': emprestimos,
                'usuario_logado': request.session.get('usuario'),
                'id_livro': id,
            }
            print(content)  # Adicione esta linha para depurar
            return render(request, 'ver_livro.html', content)
        else:
            return HttpResponse('Esse livro não é seu')
    return redirect('/auth/login/?status=2')


# Cadastro de um novo livro
def cadastrar_livro(request):
    if request.method == 'POST':
        form = CadastroLivro(request.POST)
        if form.is_valid():
            livro = form.save(commit=False)
            livro.usuario_id = request.session['usuario']
            livro.save()
            return redirect('/livro/home')
        else:
            return HttpResponse('Dados inválidos')
    else:
        form = CadastroLivro()
        return render(request, 'cadastrar_livro.html', {'form': form})


# Exclusão de um livro
def excluir_livro(request, id):
    livro = Livros.objects.get(id=id)
    if livro.usuario.id == request.session['usuario']:
        livro.delete()
        return redirect('/')
    return HttpResponse('Esse livro não é seu')


# Cadastro de uma nova categoria
def cadastrar_categoria(request):
    if request.method == 'POST':
        form = CategoriaLivro(request.POST)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.usuario_id = request.session['usuario']
            categoria.save()
            return redirect('/livro/home?cadastro_categoria=1')
        else:
            return HttpResponse('Dados inválidos')
    else:
        form = CategoriaLivro()
        return render(request, 'cadastrar_categoria.html', {'form': form})


# Cadastro de um empréstimo
def cadastrar_emprestimo(request):
    if request.method == 'POST':
        nome_emprestado = request.POST.get('nome_emprestado')
        nome_emprestado_anonimo = request.POST.get('nome_emprestado_anonimo')
        livro_emprestado = request.POST.get('livro_emprestado')
        
        emprestimo = Emprestimos(
            nome_emprestado_anonimo=nome_emprestado_anonimo if nome_emprestado_anonimo else None,
            nome_emprestado_id=nome_emprestado if nome_emprestado else None,
            livro_id=livro_emprestado
        )
        emprestimo.save()

        livro = Livros.objects.get(id=livro_emprestado)
        livro.emprestado = True
        livro.save()

        return redirect('/livro/home')


# Devolução de um livro
def devolver_livro(request):
    id_livro = request.POST.get('id_livro_devolver')
    livro = Livros.objects.get(id=id_livro)
    livro.emprestado = False
    livro.save()

    emprestimo = Emprestimos.objects.get(Q(livro=livro) & Q(data_devolucao=None))
    emprestimo.data_devolucao = datetime.now()
    emprestimo.save()

    return redirect('/livro/home')


# Alteração dos dados de um livro
def alterar_livro(request):
    livro_id = request.POST.get('livro_id')
    nome_livro = request.POST.get('nome_livro')
    autor = request.POST.get('autor')
    co_autor = request.POST.get('co_autor')
    categoria_id = request.POST.get('categoria_id')

    livro = Livros.objects.get(id=livro_id)
    if livro.usuario.id == request.session['usuario']:
        livro.nome = nome_livro
        livro.autor = autor
        livro.co_autor = co_autor
        livro.categoria_id = categoria_id
        livro.save()
        return redirect(f'/livro/ver_livro/{livro_id}')
    return HttpResponse('Esse livro não é seu')


# Visualizar seus empréstimos
def seus_emprestimos(request):
    usuario = Usuario.objects.get(id=request.session['usuario'])
    emprestimos = Emprestimos.objects.filter(nome_emprestado=usuario)

    return render(request, 'seus_emprestimos.html', {'usuario_logado': request.session['usuario'],
                                                     'emprestimos': emprestimos})


# Processamento da avaliação de um empréstimo
def processa_avaliacao(request):
    id_emprestimo = request.POST.get('id_emprestimo')
    emprestimo = Emprestimos.objects.get(id=id_emprestimo)
    avaliacao = request.POST.get('opcoes')
    emprestimo.avaliacao = avaliacao
    emprestimo.save()

    id_livro = request.POST.get('id_livro')
    return redirect(f'/livro/ver_livro/{id_livro}')
