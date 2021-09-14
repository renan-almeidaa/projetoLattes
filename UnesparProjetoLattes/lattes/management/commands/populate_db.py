from csv import ProjectExtract, xmlHandler
import time
from django.core.management.base import BaseCommand
from lattes.models import *

class Command(BaseCommand):
    args = ""
    help = "comando que popula as tabelas do banco de dados"

    def _create_pessoas(self):
        start_time = time.time()
        print("exluindo pessoas...")
        Pessoas.objects.all().delete()
        print("salvando pessoas...")
        xmlHandler.todas_pessoas()
        print(f"----{time.time() - start_time}----")

    def _create_projects(self):
        start_time = time.time()
        print("exluindo projetos...")
        Projeto.objects.all().delete()
        print("salvando projetos...")
        for p in xmlHandler.all_projects():
            p1 = Projeto(nome = p["NOME"], id_curriculo = p["IDCURRICULO"], ano_inicio = p["ANOINICIO"], situacao = p["SITUACAO"], tipo = p["TIPO"], coordenador = p["COORDENADOR"], informado_por = p["INFORMADOPOR"])
            p1.save()
        print(f"----{time.time() - start_time}----")

    def _create_productions(self):
        start_time = time.time()
        print("exluindo tabelas...")  
        Producao.objects.all().delete()
        print("salvando producoes...")
        for p in xmlHandler.all_productions():
            p1 = p.production
            p1.save()
            for setor in p.setores:
                setor.save()
            for area in p.areasConchecimento:
                area.save()
            for palavra in p.palavrasChaves:
                palavra.save()
        print(f"----{time.time() - start_time}----")

    def handle(self, *args, **options):
        self._create_pessoas()
        self._create_projects()
        self._create_productions()