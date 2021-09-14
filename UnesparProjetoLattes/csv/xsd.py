from xml.etree import ElementTree
import xmlschema
import os

CURRICULO = 'CURRICULO-VITAE'
DADOS_GERAIS = 'DADOS-GERAIS'
BIBLIOGRAFICA = 'PRODUCAO-BIBLIOGRAFICA'
TECNICA = 'PRODUCAO-TECNICA'
OUTRO = 'OUTRO-TIPO'

# CONFIGURE
FILEPATH = os.path.abspath('csv/xsdtest/Curriculo_Lattes.xsd')

def obter_dicionario(t):
    if type(t) is ElementTree.ElementTree: return obter_dicionario(t.getroot())
    return {
        **t.attrib,
        'TEXT': t.text,
        **{e.tag: obter_dicionario(e) for e in t}
    }

def buscar_elemento(nome_elemento):
    lista = obter_lista_elemento()
    for item in lista:
        if item['@name'] == nome_elemento:
            return item

def obter_lista_elemento():
    schema = xmlschema.XMLSchema(FILEPATH)
    return schema.to_dict(FILEPATH)['xs:element']

def obter_producoes():
    lista_elementos = obter_lista_elemento()
    lista_producoes = set()
    for elemento in lista_elementos:
        try:
            atributo = elemento['xs:complexType']['xs:attribute']
            sequencia = None

            if type(atributo) == dict:
                sequencia = atributo['@name']
            elif type(atributo) == list:
                for dictionary in atributo:
                    if dictionary['@name'] == 'SEQUENCIA-PRODUCAO':
                        sequencia = dictionary['@name']

            if sequencia == 'SEQUENCIA-PRODUCAO':
                lista_producoes.add(elemento['@name'])
        
        except KeyError:
            continue
    return lista_producoes

def obter_estrutura(nome_elemento):
    elemento = buscar_elemento(nome_elemento)
    lista = elemento['xs:complexType']['xs:sequence']['xs:element']
    return [item['@ref'] for item in lista ]