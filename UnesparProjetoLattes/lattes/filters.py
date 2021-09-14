from django.forms import widgets
import django_filters
from django.forms.widgets import TextInput
from .models import Producao, Pessoas, Projeto

class ProducaoFilter(django_filters.FilterSet):
    titulo = django_filters.CharFilter(field_name='titulo', lookup_expr='contains', widget=TextInput(attrs={'placeholder': 'Digite titulo'}))
    informado_por = django_filters.CharFilter(field_name='informado_por', lookup_expr='contains', widget=TextInput(attrs={'placeholder': 'Digite quem informou'}))
    tipo = django_filters.CharFilter(field_name='tipo', lookup_expr='contains', widget=TextInput(attrs={'placeholder': 'Digite tipo'}))
    tipo_agrupador = django_filters.CharFilter(field_name='tipo_agrupador', lookup_expr='contains', widget=TextInput(attrs={'placeholder': 'Digite tipo agrupador'}))
    class Meta:
        model = Producao
        fields = {
            'ano': ['gte', 'lte']
        }

class PessoasFilter(django_filters.FilterSet):
    
    
    nome = django_filters.CharFilter(field_name='nome', lookup_expr='contains', widget=TextInput(attrs={'placeholder': 'Digite nome'}))
    campus = django_filters.CharFilter(field_name='campus', lookup_expr='contains', widget=TextInput(attrs={'placeholder': 'Digite campus'}))
    titulo =  django_filters.CharFilter(field_name='titulo', lookup_expr='contains', widget=TextInput(attrs={'placeholder': 'Digite titulo'}))
    tipo_vinculo = django_filters.CharFilter(field_name='tipo_vinculo', lookup_expr='contains', widget=TextInput(attrs={'placeholder': 'Digite tipo de vinculo'}))
    
    
situacao_choices = (
    ('CONCLUIDO', 'Concluido'),
    ('EM_ANDAMENTO', 'Em Andamento')
)

tipo_choices = (
    ('DESENVOLVIMENTO', 'Desenvolvimento'),
    ('EXTENSAO', 'Extensão'),
    ('PESQUISA', 'Pesquisa'),
    ('OUTRA', 'Outra')
)

class ProjetoFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(field_name='nome', lookup_expr='contains', widget=TextInput(attrs={'placeholder': 'Digite o nome'}))
    ano_inicio = django_filters.NumberFilter(field_name='ano-inicio', widget=TextInput(attrs={'placeholder': 'Digite ano de inicio'}))
    situacao = django_filters.ChoiceFilter(field_name='situacao', choices=situacao_choices)
    tipo = django_filters.ChoiceFilter(field_name='tipo', choices=tipo_choices)
    coordenador = django_filters.CharFilter(field_name='coordenador', lookup_expr='contains', widget=TextInput(attrs={'placeholder': 'Digite o coordenador'}))
    informado_por = django_filters.CharFilter(field_name='informado_por', lookup_expr='contains', widget=TextInput(attrs={'placeholder': 'Digite quem informou'}))

