from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib.auth import authenticate as auth, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from stuff import settings
from django.contrib.auth.decorators import login_required
from .models import Anuncio, Usuario, Aluguel
from rentstuff.forms import *
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from py2neo import authenticate, Graph, Node, Relationship

def index(request):
    anuncios_novos = Anuncio.objects.order_by('-dt_inicio')[:20]
    context = {'anuncios_novos': anuncios_novos}
    return render(request, 'rentstuff/index.html', context)

@login_required
def detalhes(request, anuncio_id):
    anuncio = get_object_or_404(Anuncio, pk=anuncio_id)
    return render(request, 'rentstuff/detalhes.html', {'anuncio' : anuncio})

def usuario(request, usr):
    usuario = get_object_or_404(Usuario, username=usr)
    anuncios = usuario.anuncios.all()
    return render(request, 'rentstuff/usuario.html', {'usuario' : usuario, 'anuncios' : anuncios})

def Login(request):
    next = request.GET.get('next', '/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(next)
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)

    return render(request, "rentstuff/login.html", {'redirect_to': next})

def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = Usuario.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            email=form.cleaned_data['email'],
            cpf=form.cleaned_data['cpf']
            )
            return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })

    return render_to_response(
    'rentstuff/register.html',
    variables,
    )

@csrf_protect
@login_required
def ad(request):
    user_id = None
    if request.user.is_authenticated():
        user_id = request.user.id

    if request.method == 'POST':
        form = AdForm(request.POST)

        if form.is_valid():
            ad = Anuncio.objects.create(
            categoria = form.cleaned_data['categoria'],
            produto = form.cleaned_data['produto'],
            marca = form.cleaned_data['marca'],
            modelo = form.cleaned_data['modelo'],
            descricao = form.cleaned_data['descricao'],
            numserie = form.cleaned_data['numserie'],
            peso = form.cleaned_data['peso'],
            c_prof = form.cleaned_data['c_prof'],
            c_altura = form.cleaned_data['c_altura'],
            c_largura = form.cleaned_data['c_largura'],
            diaria = form.cleaned_data['diaria'],
            usuario_id = user_id
            )

            categoria = form.cleaned_data['categoria']
            produto = form.cleaned_data['produto']
            categorias = categoria.split('/')

            # Autentica no BD neo4j
            authenticate("localhost:7474", "neo4j", "secret")
            # Recupera o BD para uma variável
            stuffgraph = Graph()
            # Cria um node para o produto
            produto_node = Node("Produto", id=ad.id, nome=produto)
            # Monta a query Cypher para buscar a categoria
            cypher_str = 'MATCH '

            for i in range(len(categorias) - 1):
                cypher_str = cypher_str + '''(%s: Categoria {nome: "%s"})
                                            -[:TEM_SUBCATEGORIA]->''' % ("a" + str(i), categorias[i])
            cypher_str = cypher_str + '''(%s: Categoria {nome: "%s"})
            RETURN %s''' % ("a" + str(len(categorias)), categorias[len(categorias) - 1],
                            "a" + str(len(categorias)))
            # Captura em uma variável o node de categoria retornado pela query
            categoria_node = stuffgraph.cypher.execute_one(cypher_str)

            # Cria a relação ESTA_EM entre produto e categoria
            rel_produto_categoria = Relationship(produto_node, "ESTA_EM", categoria_node)

            # Persiste no BD neo4j
            stuffgraph.create(rel_produto_categoria)

            return HttpResponseRedirect('/')
    else:
        form = AdForm()
    variables = RequestContext(request, {
    'form': form
    })

    return render_to_response(
    'rentstuff/ad.html',
    variables,
    )

@login_required
def aluguel(request, ad_id):
    user_id = None
    if request.user.is_authenticated():
        user_id = request.user.id
    anuncio = get_object_or_404(Anuncio, pk=ad_id)
    if request.method == 'POST':
        form = RentForm(request.POST)
        if form.is_valid():
            dt_start = form.cleaned_data['dt_inicio']
            dt_end = form.cleaned_data['dt_fim']
            aluguel = Aluguel.objects.create(
            anuncio_id = ad_id,
            usuario_id = user_id,
            dt_inicio = form.cleaned_data['dt_inicio'],
            dt_fim = form.cleaned_data['dt_fim'],
            preco = (dt_end - dt_start).days * anuncio.diaria,
            )
            return HttpResponseRedirect('/sucesso')
    else:
        form = RentForm()
    variables = RequestContext(request, {
    'form': form
    })

    return render_to_response(
    'rentstuff/aluguel.html',
    variables,
    )

def categoria(request, cat):
    authenticate("localhost:7474", "neo4j", "secret")
    stuffgraph = Graph()
    categorias = cat.split('/')
    cypher_str = 'MATCH '
    for i in range(len(categorias) - 1):
        cypher_str = cypher_str + '''(%s: Categoria {nome: "%s"})
                    -[:TEM_SUBCATEGORIA]->''' % ("a" + str(i), categorias[i])
    cypher_str = cypher_str + '''(%s: Categoria {nome: "%s"})
                    <-[:ESTA_EM]-(p: Produto) RETURN p''' % ("a" + str(len(categorias)),
                    categorias[len(categorias) - 1])

    anuncios = stuffgraph.cypher.execute(cypher_str).to_subgraph().nodes
    anuncios_categoria = []
    for anuncio in anuncios:
        anuncios_categoria.append(get_object_or_404(Anuncio, pk=anuncio.properties["id"]))
    context = {'anuncios_categoria': anuncios_categoria, 'categoria': cat}
    return render(request, 'rentstuff/categoria.html', context)

def sucesso(request):
    return render(request, 'rentstuff/sucesso.html')
