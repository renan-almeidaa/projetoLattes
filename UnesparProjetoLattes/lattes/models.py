from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField

# Create your models here.

class Producao(models.Model):
    ano = models.IntegerField()
    informado_por = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    tipo_agrupador = models.CharField(max_length=255)
    titulo = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"TITULO = {self.titulo}, ANO = {self.ano}, INFORMADOPOR = {self.informadoPor}"

class Pessoas(models.Model):
    nome = models.CharField(max_length=255)
    campus = models.CharField(max_length=255)
    titulo = models.CharField(max_length=255)
    ano_conclusao = models.CharField(max_length=255)
    curso_formacao = models.CharField(max_length=255)
    faculdade_formacao = models.CharField(max_length=255)
    vinculo_data_inicio = models.CharField(max_length=255)
    tipo_vinculo = models.CharField(max_length=255)
    outro_vinculo = models.CharField(max_length=255)
    enquadramento = models.CharField(max_length=255)
    outro_enquadramento = models.CharField(max_length=255)
    src_image = models.ImageField(upload_to='pessoas')
    last_update = models.CharField(max_length=255)
    resumo = models.TextField()

class SetorAtividade(models.Model):
    setor = models.CharField(max_length=45)
    producao_id = models.ForeignKey(Producao, on_delete=models.CASCADE, related_name="setores_atividade")

class PalavraChave(models.Model):
    palavra = models.CharField(max_length=45)
    producao_id = models.ForeignKey(Producao, on_delete=models.CASCADE, related_name="palavrasChave")

class AreaConhecimento(models.Model):
    grande_area = models.CharField(max_length=45)
    area = models.CharField(max_length=45)
    sub_area = models.CharField(max_length=45)
    especialidade = models.CharField(max_length=45)
    producao_id = models.ForeignKey(Producao, on_delete=models.CASCADE, related_name="areas_conhecimento")

class Autor(models.Model):
    nome_completo = models.CharField(max_length=45)
    nome_citacao = models.CharField(max_length=45)
    id_CNPQ = models.CharField(max_length=45)

class ProducaoAutor(models.Model):
    producao_id = models.ForeignKey(Producao, on_delete=models.CASCADE, related_name = "producoes")
    autor_id = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name= "Autores")
    ordem_autoria = models.CharField(max_length=45)

class Projeto(models.Model):
    nome = models.CharField(max_length=50)
    id_curriculo = models.CharField(max_length=50)
    ano_inicio = models.CharField(max_length=4)
    situacao = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)
    coordenador = models.CharField(max_length=50)
    informado_por = models.CharField(max_length=50)

    def __str__(self):
        return f"(NOME: {self.nome}, INFORMADOPOR: {self.informado_por}, TIPO: {self.tipo}, ANOINICIO: {self.ano_inicio}, IDCURRICULO: {self.id_curriculo}, SITUAÇÃO:{self.situacao}, COORENADOR:{self.coordenador})"

