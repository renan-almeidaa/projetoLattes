from .production import ProductionFactory


class AbstractXml():
    def __init__(self):
        self.name = ""
        self.elements = []
        self.productions = []
        self.typeList = {"TRABALHO-EM-EVENTOS": ["Produção bibliográfica", "Trabalho publicado em anais de evento"], "ARTIGO-PUBLICADO": ["Produção bibliográfica", "Artigo publicado em periódicos"], "CAPITULO-DE-LIVRO-PUBLICADO": ["Produção bibliográfica", "Capítulo de livro publicado"], "TEXTO-EM-JORNAL-OU-REVISTA": ["Produção bibliográfica", "Texto em jornal ou revista"], "OUTRA-PRODUCAO-BIBLIOGRAFICA": ["Produção bibliográfica", "Outra produção bibliográfica"], "PREFACIO-POSFACIO": ["Produção bibliográfica", "Prefácio, Posfácio"], "TRADUCAO": ["Produção bibliográfica", "Tradução"], "PARTITURA-MUSICAL": ["Produção bibliográfica", "Partitura musical"], "LIVRO-PUBLICADO-OU-ORGANIZADO": ["Produção bibliográfica", "Livro publicado"], "DESENVOLVIMENTO-DE-MATERIAL-DIDATICO-OU-INSTRUCIONAL": ["Produção técnica", "Desenvolvimento de material didático ou instrucional"], "PROGRAMA-DE-RADIO-OU-TV": ["Produção técnica", "Programa de Rádio ou TV"], "TRABALHO-TECNICO": ["Produção técnica", "Trabalhos técnicos"], "OUTRA-PRODUCAO-TECNICA": ["Produção técnica", "Outra produção técnica"], "CURSO-DE-CURTA-DURACAO-MINISTRADO": ["Produção técnica", "Curso de curta duração ministrado"], "APRESENTACAO-DE-TRABALHO": ["Produção técnica", "Apresentação de Trabalho e palestra"], "CARTA-MAPA-OU-SIMILAR": ["Produção técnica|Cartas", "Mapas ou Similares"], "PROCESSOS-OU-TECNICAS": ["Produção técnica", "Processo ou técnica"], "PRODUTO-TECNOLOGICO": ["Produção técnica", "Produto"], "MIDIA-SOCIAL-WEBSITE-BLOG": ["Produção técnica", "Rede social, Website e blog"], "EDITORACAO": ["Produção técnica", "Editoração"], "RELATORIO-DE-PESQUISA": [
            "Produção técnica", "Relatório de pesquisa"], "SOFTWARE": ["Produção técnica", "Programa de computador"], "ARTES-CENICAS": ["Produção artística/cultural", "Artes Cênicas"], "ARTES-VISUAIS": ["Produção artística/cultural", "Artes Visuais"], "MUSICA": ["Produção artística/cultural", "Música"], "OUTRA-PRODUCAO-ARTISTICA-CULTURAL": ["Produção artística/cultural", "Artes Visuais"], "DEMAIS-TRABALHOS": ["Outro tipo de produção", "Outro tipo de produção"], "BANCA-JULGADORA-PARA-PROFESSOR-TITULAR": ["Banca", "Participação em banca de comissões julgadoras"], "PARTICIPACAO-EM-BANCA-DE-GRADUACAO": ["Banca", "Participação em banca de trabalhos de conclusão"], "PARTICIPACAO-EM-SEMINARIO": ["Evento", "Participações em eventos"], "ORGANIZACAO-DE-EVENTO": ["Evento", "Organização de evento"], "ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO": ["Orientação em andamento", "Dissertação de mestrado"], "ORIENTACAO-EM-ANDAMENTO-DE-APERFEICOAMENTO-ESPECIALIZACAO": ["Orientação em andamento", "Monografia de conclusão de curso de aperfeiçoamento/especialização"], "ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO": ["Orientação em andamento", "Tese de doutorado"], "ORIENTACAO-EM-ANDAMENTO-DE-GRADUACAO": ["Orientação em andamento", "Trabalho de conclusão de curso de graduação"], "ORIENTACAO-EM-ANDAMENTO-DE-POS-DOUTORADO": ["Orientação em andamento", "Supervisão de pós-doutorado"], "OUTRAS-ORIENTACOES-EM-ANDAMENTO": ["Orientação em andamento", "Orientação de outra natureza"], "ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA": ["Orientação em andamento", "Iniciação Científica"], "PATENTE": ["Produção técnica", "Patentes e registros"]}

    def addElement(self, element):
        self.elements.append(element)

    def addProduction(self, production):
        self.productions.append(production)

    def hasElement(self, element):
        if element in self.elements:
            return True
        return False

    def getElement(self, idx):
        return self.elements.__getitem__(idx)

    def getProduction(self, idx):
        return self.productions.__getitem__(idx)

    def getProductions(self):
        data = ProductionFactory.get_production("")
        dic = {}
        tmp = []
        reportedBy = self.getElement(-1).attrs.getValue(data.reportedBy)
        for producao in self.productions:
            data = ProductionFactory.get_production(producao.name)
            dic["TIPO"] = self.typeList.get(producao.name)[1]
            dic["TIPOAGRUPADOR"] = self.typeList.get(producao.name)[0]
            for dados in producao.childs:
                if dados.name.find("DADOS-BASICOS") != -1:
                    try:
                        dic["ANO"] = dados.attrs.getValue(data.year)
                        dic["TITULO"] = dados.attrs.getValue(data.title)
                        dic["INFORMADOPOR"] = reportedBy
                    except KeyError as _e:
                        print(f"this key({_e}) not exist.")
            tmp.append(dic)
            dic = {}
        return tmp

    def __str__(self):
        str = '['
        for e in self.elements:
            str += e.__str__()+', '
        return str+']'


class Element():

    def __init__(self, name, attrs):
        self.name = name
        self.childs = []
        self.attrs = attrs

    def __str__(self):
        c = ''
        for ch in self.childs:
            c += ch.__str__()+'\n'
        return f"({self.name} ATRIBUTOS:{self.attrs.items()}\n FILHOS:{c}"
