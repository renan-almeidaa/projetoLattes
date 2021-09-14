import xml.sax
import re
from lattes.models import Projeto 

class ProjectHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.projects = []
        self.project = Projeto()
        self.data = Data()
        self.extract = False
        self.reportedBy = ''
        self.IDCurriculo = None

    def startDocument(self):
        docName = self._locator.getSystemId()
        self.IDCurriculo = re.split('[./]', docName)[-2]

    def startElement(self, name, attrs):
        if name == "PROJETO-DE-PESQUISA":
            self.extract = True
            self.project.Nome = attrs.getValue(self.data.name)
            self.project.AnoInicio = attrs.getValue(self.data.year)
            self.project.situacao = attrs.getValue(self.data.situation)
            self.project.tipo = attrs.getValue(self.data.nature)

        if name == "DADOS-GERAIS":
            self.reportedBy = attrs.getValue(self.data.reportedBy)

        if self.extract:
            if name.find("INTEGRANTES-DO-PROJETO") != -1 and attrs.getValue("FLAG-RESPONSAVEL")=="SIM":
                self.project.coordenador = attrs.getValue("NOME-COMPLETO")

    def endElement(self, name):
        if name in "PROJETO-DE-PESQUISA":
            self.extract = False
            self.project.informadoPor = self.reportedBy
            self.project.IDCurriculo = self.IDCurriculo
            self.projects.append(self.project)
            self.project = Projeto()
    
    def endDocument(self):
        # for p in self.projects:  
        #     print(p)
        #     p = Projeto(Nome=p.Nome, InformadoPor=p.InformadoPor, Tipo=p.Tipo, AnoInicio=p.AnoInicio, IDCurriculo=p.IDCurriculo, Situacao=p.Situacao, Coordenador=p.Coordenador)
        #     p.save()
        pass

class Data():   
    def __init__(self):
        self.name = "NOME-DO-PROJETO"
        self.year = "ANO-INICIO"
        self.situation  = "SITUACAO"
        self.nature = "NATUREZA"
        self.reportedBy = "NOME-COMPLETO"
        self.ID = "NUMERO-IDENTIFICADOR"

def all_projects():
    print("starting...")
    handler = ProjectHandler()
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)
    parser.parse("csv/0542377388398311.xml")
    print("done...")
    return handler.projects