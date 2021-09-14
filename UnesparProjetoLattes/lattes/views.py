from django.shortcuts import render, reverse
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Producao, Pessoas, Projeto, AreaConhecimento
from .filters import ProducaoFilter, PessoasFilter, ProjetoFilter
import re

def grande_areas(list):
    result = []
    for dictionary in list:
        grande_area = dictionary['grande_area']
        area = dictionary['area']
        total = dictionary['total']
        if not grande_area in [dictionary['grande_area'] for dictionary in result]:
            result.append({'grande_area':grande_area, 'total':total})
        else:
            for dictionary in result:
                if dictionary['grande_area'] == grande_area:
                    index = result.index(dictionary)
                    result.__setitem__(index, {'grande_area':grande_area, 'total':total + result.__getitem__(index)['total']})
    return result

def valid_param(param):
    return param != '' and param != None and param != 'None'

# Create your views here.
@login_required
def pessoas(request):
    context = {}
    regex = re.compile('(-?[A-Za-z]*)')
    unicode = re.compile('[A-Za-z_Á-û]*')
    ordenar = regex.match(str(request.GET.get('ordenar'))).group()
    pessoas = Pessoas.objects.all()
    if ordenar == 'None':
        ordenar = 'nome'
    pessoas_filtradas = PessoasFilter(
       request.GET,
       queryset=pessoas.order_by(ordenar)
    )
    p = Paginator(pessoas_filtradas.qs, 10)
    page_number = request.GET.get('page')
    page_pessoas = p.get_page(page_number)
    
    context["page_pessoas"] = page_pessoas
    context["pessoas_filtradas"] = pessoas_filtradas
   
    return render(request, "lattes/pessoas/pessoas.html", context)

@login_required
def producoes(request):
    context = {}
    regex = re.compile('(-?[A-Za-z]*)')
    unicode = re.compile('[A-Za-z_Á-û]*')
    ordenar = regex.match(str(request.GET.get('ordenar'))).group()
    area = request.GET.get('area')
    grande_area = request.GET.get('grandeArea')

    if ordenar == 'None':
        ordenar = 'titulo'
    
    producoes = Producao.objects.all()
    if valid_param(grande_area):
        producoes = producoes.filter(areas_conhecimento__grande_area=grande_area)
    elif valid_param(area):
        producoes = producoes.filter(areas_conhecimento__area=area)
    
    producoes_filtrada = ProducaoFilter(
        request.GET,
        queryset=producoes.order_by(ordenar)
    )

    paginator = Paginator(producoes_filtrada.qs, 10)
    page_number = request.GET.get('page')
    producoes_page = paginator.get_page(page_number)
    areas = AreaConhecimento.objects.all().values('grande_area', 'area').annotate(total=Count('id'))
    context["areas"] = areas
    context["grande_areas"] = grande_areas(areas)
    context["producoes"] = zip(producoes_page ,[producao.palavrasChave.all() for producao in producoes_page.object_list], [producao.areas_conhecimento.all() for producao in producoes_page.object_list], [producao.setores_atividade.all() for producao in producoes_page.object_list])
    context["Producao_page"] = producoes_page
    context["producoes_filtradas"] = producoes_filtrada

    return render(request, "lattes/producoes/producoes.html", context)

@login_required
def perfilProducao(request):
    context = {}

    producoes_filtradas = ProducaoFilter(
        request.GET,
        queryset=Producao.objects.all()
    )

    query = producoes_filtradas.qs.values('ano').annotate(total=Count('id')).order_by('ano')
    context['anos'] = [dic['ano'] for dic in query]
    context['totalAno'] = [dic['total'] for dic in query]

    query = producoes_filtradas.qs.values('tipo').annotate(total=Count('id')).order_by('tipo').filter(tipo_agrupador='Produção bibliográfica')
    context['tiposB'] = [dic['tipo'] for dic in query]
    context['totalTipoB'] = [dic['total'] for dic in query]

    query = producoes_filtradas.qs.values('tipo').annotate(total=Count('id')).order_by('tipo').filter(tipo_agrupador='Produção técnica')
    context['tiposT'] = [dic['tipo'] for dic in query]
    context['totalTipoT'] = [dic['total'] for dic in query]

    query = producoes_filtradas.qs.values('tipo').annotate(total=Count('id')).order_by('tipo').filter(tipo_agrupador='Orientação em andamento')
    context['tiposO'] = [dic['tipo'] for dic in query]
    context['totalTipoO'] = [dic['total'] for dic in query]

    query = producoes_filtradas.qs.values('tipo').annotate(total=Count('id')).order_by('tipo').filter(tipo_agrupador='Produção artística/cultural')
    context['tiposA'] = [dic['tipo'] for dic in query]
    context['totalTipoA'] = [dic['total'] for dic in query]

    query = producoes_filtradas.qs.values('tipo').annotate(total=Count('id')).order_by('tipo').filter(Q(tipo_agrupador ='Banca') | Q(tipo_agrupador='Evento') | Q(tipo_agrupador='Outro tipo de produção'))
    context['tiposE'] = [dic['tipo'] for dic in query]
    context['totalTipoE'] = [dic['total'] for dic in query]

    context["producoes_filtradas"] = producoes_filtradas
    return render(request, "lattes/producoes/perfilProducao.html", context)

@login_required
def projetos(request):
    context = {}
    regex = re.compile('(-?[A-Za-z]*)')
    ordenar = regex.match(str(request.GET.get('ordenar'))).group()
    
    if ordenar == 'None':
        ordenar = 'nome'

    projetos_filtradas = ProjetoFilter(
        request.GET,
        queryset=Projeto.objects.all().order_by(ordenar)
    )
    
    p = Paginator(projetos_filtradas.qs, 10)
    page_number = request.GET.get('page')
    projeto_page = p.get_page(page_number)

    context["projeto_page"] = projeto_page
    context["projetos_filtradas"] = projetos_filtradas

    return render(request, "lattes/projetos/projetos.html", context)

def login_view(request):
    if request.method == "POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("lattes:pessoas"))
        else:
            return render(request, "lattes/login.html",{
                "message":"usuário ou senha errado."
            })
    return render(request, "lattes/login.html")

@login_required
def logout_view(request):
    logout(request)
    return render(request, "lattes/login.html")