from django.contrib import admin
from .models import *

# Register your models here.
class PessoasAdmin(admin.ModelAdmin):
    list_display = ("nome", "titulo", "campus", "ano_conclusao", "curso_formacao","faculdade_formacao", "vinculo_data_inicio", "enquadramento")

class ProducaoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "ano", "informado_por", "tipo", "tipo_agrupador")

class ProjetoAdmin(admin.ModelAdmin):
    list_display = ("nome", "id_curriculo", "ano_inicio", "situacao", "tipo", "coordenador", "informado_por")

class SetorAtividadeAdmin(admin.ModelAdmin):
    list_display = ("setor", "producao_id")

class PalavraChaveAdmin(admin.ModelAdmin):
    list_display = ("palavra", "producao_id")

class AreaConhecimentoAdmin(admin.ModelAdmin):
    list_display = ("sub_area", "area", "grande_area", "especialidade", "producao_id")


admin.site.register(Producao, ProducaoAdmin)
admin.site.register(Projeto, ProjetoAdmin)
admin.site.register(Pessoas, PessoasAdmin)
admin.site.register(SetorAtividade, SetorAtividadeAdmin)
admin.site.register(PalavraChave, PalavraChaveAdmin)
admin.site.register(AreaConhecimento, AreaConhecimentoAdmin)