from django.db.utils import IntegrityError
from csv.xsd import DADOS_GERAIS
from xml.etree import ElementTree
from csv.AbstractXml import AbstractXml, Element
from csv.production import ProductionFactory
from lattes import models
from pprint import pprint
import xml.sax, re, os

typeList = {"TRABALHO-EM-EVENTOS": ["Produção bibliográfica", "Trabalho publicado em anais de evento"], "ARTIGO-PUBLICADO": ["Produção bibliográfica", "Artigo publicado em periódicos"], "CAPITULO-DE-LIVRO-PUBLICADO": ["Produção bibliográfica", "Capítulo de livro publicado"], "TEXTO-EM-JORNAL-OU-REVISTA": ["Produção bibliográfica", "Texto em jornal ou revista"], "OUTRA-PRODUCAO-BIBLIOGRAFICA": ["Produção bibliográfica", "Outra produção bibliográfica"], "PREFACIO-POSFACIO": ["Produção bibliográfica", "Prefácio, Posfácio"], "TRADUCAO": ["Produção bibliográfica", "Tradução"], "PARTITURA-MUSICAL": ["Produção bibliográfica", "Partitura musical"], "LIVRO-PUBLICADO-OU-ORGANIZADO": ["Produção bibliográfica", "Livro publicado"], "DESENVOLVIMENTO-DE-MATERIAL-DIDATICO-OU-INSTRUCIONAL": ["Produção técnica", "Desenvolvimento de material didático ou instrucional"], "PROGRAMA-DE-RADIO-OU-TV": ["Produção técnica", "Programa de Rádio ou TV"], "TRABALHO-TECNICO": ["Produção técnica", "Trabalhos técnicos"], "OUTRA-PRODUCAO-TECNICA": ["Produção técnica", "Outra produção técnica"], "CURSO-DE-CURTA-DURACAO-MINISTRADO": ["Produção técnica", "Curso de curta duração ministrado"], "APRESENTACAO-DE-TRABALHO": ["Produção técnica", "Apresentação de Trabalho e palestra"], "CARTA-MAPA-OU-SIMILAR": ["Produção técnica|Cartas", "Mapas ou Similares"], "PROCESSOS-OU-TECNICAS": ["Produção técnica", "Processo ou técnica"], "PRODUTO-TECNOLOGICO": ["Produção técnica", "Produto"], "MIDIA-SOCIAL-WEBSITE-BLOG": ["Produção técnica", "Rede social, Website e blog"], "EDITORACAO": ["Produção técnica", "Editoração"], "RELATORIO-DE-PESQUISA": ["Produção técnica", "Relatório de pesquisa"], "SOFTWARE": ["Produção técnica", "Programa de computador"], "ARTES-CENICAS": ["Produção artística/cultural", "Artes Cênicas"], "ARTES-VISUAIS": ["Produção artística/cultural", "Artes Visuais"], "MUSICA": ["Produção artística/cultural", "Música"], "OUTRA-PRODUCAO-ARTISTICA-CULTURAL": ["Produção artística/cultural", "Artes Visuais"], "DEMAIS-TRABALHOS": ["Outro tipo de produção", "Outro tipo de produção"], "BANCA-JULGADORA-PARA-PROFESSOR-TITULAR": ["Banca", "Participação em banca de comissões julgadoras"], "PARTICIPACAO-EM-BANCA-DE-GRADUACAO": ["Banca", "Participação em banca de trabalhos de conclusão"], "PARTICIPACAO-EM-SEMINARIO": ["Evento", "Participações em eventos"], "ORGANIZACAO-DE-EVENTO": ["Evento", "Organização de evento"], "ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO": ["Orientação em andamento", "Dissertação de mestrado"], "ORIENTACAO-EM-ANDAMENTO-DE-APERFEICOAMENTO-ESPECIALIZACAO": ["Orientação em andamento", "Monografia de conclusão de curso de aperfeiçoamento/especialização"], "ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO": ["Orientação em andamento", "Tese de doutorado"], "ORIENTACAO-EM-ANDAMENTO-DE-GRADUACAO": ["Orientação em andamento", "Trabalho de conclusão de curso de graduação"], "ORIENTACAO-EM-ANDAMENTO-DE-POS-DOUTORADO": ["Orientação em andamento", "Supervisão de pós-doutorado"], "OUTRAS-ORIENTACOES-EM-ANDAMENTO": ["Orientação em andamento", "Orientação de outra natureza"], "ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA": ["Orientação em andamento", "Iniciação Científica"], "PATENTE": ["Produção técnica", "Patentes e registros"]}


class ProductionHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.file = AbstractXml()
        self.extract = False

    def startDocument(self):
        docName = self._locator.getSystemId()
        self.file.name = re.split('[./]', docName)[-2]

    def startElement(self, name, attrs):
        if self.extract:
           self.file.getProduction(-1).childs.append(Element(name, attrs))

        if name in self.file.typeList.keys():
            self.extract = True
            self.file.addProduction(Element(name, attrs))
        if name == "DADOS-GERAIS":
            self.file.addElement(Element(name,attrs))

    def endElement(self, name):
        if name in self.file.typeList.keys():
            self.extract = False   

    def endDocument(self):
        pass

class ProjectHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.projects = []
        self.project = {}
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
            self.project["NOME"] = attrs.getValue(self.data.name)
            self.project["ANOINICIO"] = attrs.getValue(self.data.year)
            self.project["SITUACAO"] = attrs.getValue(self.data.situation)
            self.project["TIPO"] = attrs.getValue(self.data.nature)

        if name == "DADOS-GERAIS":
            self.reportedBy = attrs.getValue(self.data.reportedBy)

        if self.extract:
            if name.find("INTEGRANTES-DO-PROJETO") != -1 and attrs.getValue("FLAG-RESPONSAVEL")=="SIM":
                self.project["COORDENADOR"] = attrs.getValue("NOME-COMPLETO")

    def endElement(self, name):
        if name in "PROJETO-DE-PESQUISA":
            self.extract = False
            self.project["INFORMADOPOR"] = self.reportedBy
            self.project["IDCURRICULO"] = self.IDCurriculo
            self.projects.append(self.project)
            self.project = {}
    
    def endDocument(self):
        pass

class Data():
    def __init__(self):
        self.name = "NOME-DO-PROJETO"
        self.year = "ANO-INICIO"
        self.situation  = "SITUACAO"
        self.nature = "NATUREZA"
        self.reportedBy = "NOME-COMPLETO"
        self.ID = "NUMERO-IDENTIFICADOR"

class Production():
    def __init__(self) -> None:
        self.autores = []
        self.setores = []
        self.areasConchecimento = []
        self.palavrasChaves = []
        self.sequencia = 0
        self.production = models.Producao()

    def adcionarAutor(self, autor):
        self.autores.append(autor)

    def adcionarPalavra(self, palavra):
        if palavra.palavra != '':
            self.palavrasChaves.append(palavra)

    def adcionarSetor(self, setor):
        if setor.setor != '':
            self.setores.append(setor)
    
    def adcionarAreaConhecimento(self, areaConhecimento):
        self.areasConchecimento.append(areaConhecimento)

XML_DIR = "csv/xmlstest"

def todas_pessoas():
    for file in os.listdir(XML_DIR):
        salvar_pessoa(os.path.join(XML_DIR, file))

def all_projects():
    print("starting get_all_projects...")
    tmp = []
    for file in os.listdir(XML_DIR):
        tmp = tmp + get_project(f"{XML_DIR}/{file}")
    print("done...")
    return tmp

def all_productions():
    print("starting get_all_productions...")
    tmp = []
    for file in os.listdir(XML_DIR):
        list = get_productions_from_xml(os.path.join(XML_DIR, file))
        if  list:
            tmp = tmp + list
    print("done...")
    return tmp

def get_project(filePath):
    handler = ProjectHandler()
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)
    parser.parse(filePath)
    return handler.projects

def get_production(filepath):
    handler = ProductionHandler()
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)
    parser.parse(filepath)
    return handler.file.getProductions()

def get_productions_from_xml(filepath):
    dom = ElementTree.parse(filepath)
    dados_gerais = dom.find("DADOS-GERAIS")
    
    id = filepath.split('/')[-1].split('.')[0]
    tmp = []
    for element in dom.iter():
        if element.tag in typeList.keys() and "PARTICIPACAO-EM-SEMINARIO" != element.tag:
            producao = Production()
            data = ProductionFactory.get_production(element.tag)
            sequencia = element.get('SEQUENCIA')

            producao.production.tipo = typeList[element.tag].__getitem__(1)        
            producao.production.tipo_agrupador = typeList[element.tag].__getitem__(0)
            producao.production.informado_por = dados_gerais.get("NOME-COMPLETO")

            for childs in list(element):        
                if childs.tag.find("DADOS-BASICOS") != -1:
                    try:
                        producao.production.ano = childs.get(data.year)
                        producao.production.titulo = childs.get(data.title)
                    except KeyError as _e:
                        print(f"this key({_e}) not exist.")
                    break

            for autor in element.findall('AUTORES'):
                nomeCompleto = autor.get("NOME-COMPLETO-DO-AUTOR")
                try:
                    producao.adcionarAutor(models.Autor(nome_completo=nomeCompleto, nome_citacao=autor.attrib["NOME-PARA-CITACAO"], id_CNPQ=autor.attrib["NRO-ID-CNPQ"]))
                except KeyError:
                    print(f"ERRO - não foi possivel extrair o IDCNPQ da producao SEQUENCIA({sequencia}) no arquivo {id}.xml")
            palavra_chave = element.find('PALAVRAS-CHAVE')
            if palavra_chave != None:
                producao.adcionarPalavra(models.PalavraChave(palavra=palavra_chave.attrib["PALAVRA-CHAVE-1"], producao_id=producao.production))
                producao.adcionarPalavra(models.PalavraChave(palavra=palavra_chave.attrib["PALAVRA-CHAVE-2"], producao_id=producao.production))
                producao.adcionarPalavra(models.PalavraChave(palavra=palavra_chave.attrib["PALAVRA-CHAVE-3"], producao_id=producao.production))
                producao.adcionarPalavra(models.PalavraChave(palavra=palavra_chave.attrib["PALAVRA-CHAVE-4"], producao_id=producao.production))
                producao.adcionarPalavra(models.PalavraChave(palavra=palavra_chave.attrib["PALAVRA-CHAVE-5"], producao_id=producao.production))
                producao.adcionarPalavra(models.PalavraChave(palavra=palavra_chave.attrib["PALAVRA-CHAVE-6"], producao_id=producao.production))
            setor_atividade = element.find('SETORES-DE-ATIVIDADE')
            if(setor_atividade != None):
                producao.adcionarSetor(models.SetorAtividade(setor=setor_atividade.attrib["SETOR-DE-ATIVIDADE-2"], producao_id=producao.production))
                producao.adcionarSetor(models.SetorAtividade(setor=setor_atividade.attrib["SETOR-DE-ATIVIDADE-1"], producao_id=producao.production))
                producao.adcionarSetor(models.SetorAtividade(setor=setor_atividade.attrib["SETOR-DE-ATIVIDADE-3"], producao_id=producao.production))  
            areas_conhecimento = element.find('AREAS-DO-CONHECIMENTO')
            if(areas_conhecimento):
                for area_conhecimento in list(areas_conhecimento):
                    producao.adcionarAreaConhecimento(models.AreaConhecimento(area=area_conhecimento.attrib["NOME-DA-AREA-DO-CONHECIMENTO"], sub_area=area_conhecimento.attrib["NOME-DA-SUB-AREA-DO-CONHECIMENTO"], grande_area=area_conhecimento.attrib["NOME-GRANDE-AREA-DO-CONHECIMENTO"], especialidade=area_conhecimento.attrib["NOME-DA-ESPECIALIDADE"], producao_id=producao.production))
            tmp.append(producao)
    return tmp

#QNAME
DADOS_GERAIS = 'DADOS-GERAIS'
RESUMO = 'RESUMO-CV'
ATUACAO_PROFISSIONAL = 'ATUACOES-PROFISSIONAIS'
VINCULOS = 'VINCULOS'
ENDERECO = 'ENDERECO'
ENDERECO_PROFISSIONAL = 'ENDERECO-PROFISSIONAL'
#ATRIBUTOS
ATUALIZACAO = 'DATA-ATUALIZACAO'
NOME = 'NOME-COMPLETO'
TEXTO_RESUMO = 'TEXTO-RESUMO-CV-RH'
TITULACAO = 'FORMACAO-ACADEMICA-TITULACAO'
STATUS_TITULACAO = 'STATUS-DO-CURSO'
ANO_DE_CONCLUSAO = 'ANO-DE-CONCLUSAO'
NOME_INSTITUICAO = 'NOME-INSTITUICAO'
NOME_CURSO = 'NOME-CURSO'
ENQUADRAMENTO = 'ENQUADRAMENTO-FUNCIONAL'
OUTRO_ENQUADRAMENTO = 'OUTRO-ENQUADRAMENTO-FUNCIONAL-INFORMADO'
TIPO_VINCULO = 'TIPO-DE-VINCULO'
OUTRO_VINCULO = 'OUTRO-VINCULO-INFORMADO'
ANO_INICIO = 'ANO-INICIO'
CIDADE = 'CIDADE'

SIGLA_UNESPAR = 'UNESPAR'
UNESPAR = 'UNIVERSIDADE ESTADUAL DO PARANÁ'
#SIGLA_FECEA = 'FECEA'
#FECEA = 'FACULDADE ESTADUAL DE CIÊNCIAS ECONÔMICAS DE APUCARANA'

cidade_choices = (
    'APUCARANA',
    'CAMPO MOURÃO',
    'CAMPO MOURAO',
    'CURITIBA',
    'PARANAGUÁ',
    'PARANAGUA',
    'PARANAVAÍ',
    'PARANAVAI',
    'UNIÃO DA VITÓRIA',
    'UNIAO DA VITORIA',
    'GUATUPÊ',
    'GUATUPE'
)

def definir_campus(endereco, id):
    cidade = endereco.get(CIDADE)
    cidade_upper = cidade.upper()

    if cidade is not None and cidade_upper in cidade_choices:
        return cidade
    print(f"ERRO - não foi possivel indentificar o campus do arquivo {id}.xml")
    return ''

def definir_vinculo(atuacoes, id):
    vinculo_recente = {
        ENQUADRAMENTO: '',
        OUTRO_ENQUADRAMENTO: '', 
        TIPO_VINCULO: '',
        OUTRO_VINCULO: '',
        ANO_INICIO: ''
    }
    maior_ano = -1
    for item in atuacoes:
        instituicao = item.get(NOME_INSTITUICAO)
        instituicao_upper = instituicao.upper()
        if instituicao_upper.find(SIGLA_UNESPAR) != -1 or instituicao_upper.find(UNESPAR) != -1:
            vinculos = item.findall(VINCULOS)
            for vinculo in vinculos:
                ano_inicio = int(vinculo.get(ANO_INICIO))
                if maior_ano < ano_inicio:
                    maior_ano = ano_inicio
                    vinculo_recente = {
                        ENQUADRAMENTO: vinculo.get(ENQUADRAMENTO),
                        OUTRO_ENQUADRAMENTO: vinculo.get(OUTRO_ENQUADRAMENTO), 
                        TIPO_VINCULO: vinculo.get(TIPO_VINCULO),
                        OUTRO_VINCULO: vinculo.get(OUTRO_VINCULO),
                        ANO_INICIO: ano_inicio
                    }
    if maior_ano == -1:
        print(f"ERRO - não foi possivel indentificar o vinculo do arquivo {id}.xml")
    return vinculo_recente

def definir_titulacao(list, id):
    for item in list[::-1]:
        if item.get(STATUS_TITULACAO) == "CONCLUIDO":
            titulacao = item.tag
            ano_conclusao = item.get(ANO_DE_CONCLUSAO)
            nome_instituicao = item.get(NOME_INSTITUICAO)
            nome_curso = item.get(NOME_CURSO)
            return {
                TITULACAO: titulacao if titulacao is not None else '',
                ANO_DE_CONCLUSAO: ano_conclusao if ano_conclusao is not None else '',
                NOME_INSTITUICAO: nome_instituicao if nome_instituicao is not None else '',
                NOME_CURSO: nome_curso if nome_curso is not None else '' 
            }
    print(f"ERRO - não foi possivel extrair a titulação do arquivo {id}.xml")        
    return {
        TITULACAO: '',
        ANO_DE_CONCLUSAO: '',
        NOME_INSTITUICAO: '',
        NOME_CURSO: ''
    }

def salvar_pessoa(filepath):
    dom = ElementTree.parse(filepath)
    dados_gerais = dom.find(DADOS_GERAIS)
    resumo = dados_gerais.find(RESUMO)
    titulacao = dados_gerais.find(TITULACAO)
    atuacoes = dados_gerais.find(ATUACAO_PROFISSIONAL)
    enderecos = dados_gerais.find(ENDERECO)
    endereco_profissional = enderecos.find(ENDERECO_PROFISSIONAL)

    id = filepath.split('/')[-1].split('.')[0]
    texto_resumo = resumo.get(TEXTO_RESUMO) if resumo is not None else ''
    if resumo is None:
        print(f"ERRO - não foi possivel extrair o resumo do arquivo {id}.xml")

    nome = dados_gerais.get(NOME)
    data_atualizacao = dom.getroot().get(ATUALIZACAO)
    titulo = definir_titulacao(list(titulacao), id)
    vinculo = definir_vinculo(list(atuacoes), id)

    campus = definir_campus(endereco_profissional, id) if endereco_profissional is not None else ''

    try:
        models.Pessoas.objects.create(nome=nome, campus=campus,titulo=titulo[TITULACAO], ano_conclusao=titulo[ANO_DE_CONCLUSAO], curso_formacao=titulo[NOME_CURSO], faculdade_formacao=titulo[NOME_INSTITUICAO], resumo=texto_resumo, vinculo_data_inicio=vinculo[ANO_INICIO], tipo_vinculo=vinculo[TIPO_VINCULO], outro_vinculo=vinculo[OUTRO_VINCULO], enquadramento=vinculo[ENQUADRAMENTO], outro_enquadramento=vinculo[OUTRO_ENQUADRAMENTO], last_update=data_atualizacao)
    except KeyError as _e:
        print(f"KEYERROR {_e} - não foi possivel salvar o  arquivo {id}.xml")
    except IntegrityError as _e:
        print(f"INTEGRITYERROR {_e} - não foi possivel salvar o arquivo {id}.xml")