from abc import ABCMeta, abstractstaticmethod

class ProductionFactory():

    @staticmethod
    def get_production(type):
        if type == "TRABALHO-EM-EVENTOS":
            return TrabalhoEvento()
        elif type == "ARTIGO-PUBLICADO":
            return ArtigoPublicado()
        elif type == "CAPITULO-DE-LIVRO-PUBLICADO":
            return CapituloLivro() 
        elif type == "TEXTO-EM-JORNAL-OU-REVISTA":
            return TextoJornalRevista()
        elif type == "LIVRO-PUBLICADO-OU-ORGANIZADO":
            return LivroPublicado()
        elif type == "PROCESSOS-OU-TECNICAS":
            return ProcessoTecnica()
        elif type == "PATENTE":
            return PatenteRegistro()
        elif type == "PRODUTO-TECNOLOGICO":
            return Produto()
        elif type == "SOFTWARE":
            return Software()
        elif type == "TRABALHO-TECNICO":
            return TrabalhoTecnico()
        elif type.find("ORIENTACAO-EM-ANDAMENTO") != -1  or type== "OUTRAS-ORIENTACOES-EM-ANDAMENTO":
            return OrientacaoAndamento()
        elif False:
            pass
        else:
            return IProduction()

class IProduction(metaclass=ABCMeta):
    
    def __init__(self):
        self.title = "TITULO"
        self.year = "ANO"
        self.type = "Não identificado"
        self.groupType = "Não identificado"
        self.reportedBy = "NOME-COMPLETO"

class TrabalhoEvento(IProduction):
    def __init__(self):
        super().__init__()
        self.title = "TITULO-DO-TRABALHO"
        self.year = "ANO-DO-TRABALHO"

    def get_production(self):
        print("Isso e um trabalho em evento")

class ArtigoPublicado(IProduction):
    def __init__(self):
        super().__init__()
        self.title = "TITULO-DO-ARTIGO"
        self.year = "ANO-DO-ARTIGO"

class CapituloLivro(IProduction):
    def __init__(self):
        super().__init__()
        self.title = "TITULO-DO-CAPITULO-DO-LIVRO"

class TextoJornalRevista(IProduction):
    def __init__(self):
        super().__init__()
        self.title = "TITULO-DO-TEXTO"
        self.year = "ANO-DO-TEXTO"

class LivroPublicado(IProduction):
    def __init__(self):
        super().__init__()
        self.title = "TITULO-DO-LIVRO"

class ProcessoTecnica(IProduction):
    def __init__(self):
        super().__init__()
        self.title = "TITULO-DO-PROCESSO"

class PatenteRegistro(IProduction):

    def __init__(self):
        super().__init__()
        self.year = "ANO-DESENVOLVIMENTO"

class Produto(IProduction):
    def __init__(self):
        super().__init__()
        self.title = "TITULO-DO-PRODUTO"

class Software(IProduction):
    def __init__(self):
        super().__init__()
        self.title = "TITULO-DO-SOFTWARE"

class OrientacaoAndamento(IProduction):
    def __init__(self):
        super().__init__()
        self.title = "TITULO-DO-TRABALHO"

class TrabalhoTecnico(IProduction):
    def __init__(self):
        super().__init__()
        self.title = "TITULO-DO-TRABALHO-TECNICO"