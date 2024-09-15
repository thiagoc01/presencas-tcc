import unidecode
import requests
import re
from presencas import app
from datetime import date

class Artista:

    def __init__(self, form, arquivos):

        self.nome = ""
        self.sobrenome = ""
        self.nome_completo = ""
        self.imagens = {}
        self.descricao = ""
        self.links = []
        self.atualizacao = ""
        self.genero = ""
        self.pesquisante = ""
        self.email_pesquisante = ""
        self.data_nascimento = ""
        self.palavras_chave = []
        self.pagina = ""

        self._inicializa_artista(form, arquivos)

    def _carrega_imagens(self, form, arquivos):

        for campo in form.imagens:

            if campo.titulo == None or campo.titulo.data == '':

                titulo = arquivos.get(campo.name + '-arquivo').filename

                if titulo.find('_retrato') != -1:

                    titulo = self.nome_completo

            else:
                titulo = campo.titulo.data

            self.imagens[titulo] = {}
            self.imagens[titulo]['nome_arquivo'] = campo.name + '-arquivo'
            self.imagens[titulo]['descricao'] = campo.descricao.data

            self.imagens[titulo]['titulo'] = titulo

            if campo.material.data:
                self.imagens[titulo]['descricao'] += ("\n<br>\n" + campo.material.data) \
                        if self.imagens[titulo]["descricao"] != "" else campo.material.data
                
            if campo.tamanho.data:
            
                self.imagens[titulo]['descricao'] += ("\n<br>\n" + campo.tamanho.data) \
                        if self.imagens[titulo]["descricao"] != "" else campo.tamanho.data
                
            if campo.outras_infos.data:

                self.imagens[titulo]['descricao'] += ("\n<br>\n" + campo.outras_infos.data) \
                        if self.imagens[titulo]["descricao"] != "" else campo.outras_infos.data
            
            if campo.tamanho.data:
            
                eArea = re.compile("[0-9\,]{1,5} *[xX] *[0-9\,]{1,5} *(cm)?")
                eComprimento = re.compile("[0-9]{1,3}(?= *cm)")

                if eArea.match(campo.tamanho.data):
                    self.imagens[titulo]['area'] = campo.tamanho.data

                elif eComprimento.search(campo.tamanho.data):
                    achado = eComprimento.search(campo.tamanho.data)
                    self.imagens[titulo]['comprimento'] = float(achado.group(0)) / 100.0
            
            if campo.data.data:

                self.imagens[titulo]['ano'] = campo.data.data

            if campo.fonte.data:

                self.imagens[titulo]['fonte'] = campo.fonte.data                


    def _inicializa_artista(self, form, arquivos):

        nome = self.nome_completo = form.nome.data

        if len(nome.split(" ")) == 2:
            self.nome, self.sobrenome = nome.split(" ")
        else:
            self.nome, self.sobrenome = nome.split(" ")[0], " ".join(nome.split()[1:])

        self._carrega_imagens(form, arquivos)

        self.descricao = f"**Trajetória**\n<br>\n {form.trajetoria.data}"
        self.descricao += f"\n<br>\n**Produção**\n<br>\n {form.producao.data}"

        for campo in form.links:

            self.links.append(campo.url.data)

        if form.ultima_atualizacao.data:

            self.atualizacao = date.strftime(form.ultima_atualizacao.data, "%d/%m/%Y")

        if form.genero.data:

            self.genero = form.genero.data

        if form.data_nascimento.data:

            self.data_nascimento = form.data_nascimento.data

        if form.email_pesquisante.data:

            self.email_pesquisante = form.email_pesquisante.data

        if form.pesquisante.data:

            self.pesquisante = form.pesquisante.data

        if form.pagina.data:

            self.pagina = form.pagina.data

        for palavra_chave in form.palavras_chave:

            self.palavras_chave.append(palavra_chave.palavra_chave.data)

def imprime_vermelho(string): print("\033[91m{}\033[00m".format(string))
 
def imprime_verde(string): print("\033[92m{}\033[00m".format(string))

class Requisicoes:
    
    def __init__(self, token : str):
        self.header = {"Authorization" : token}
        self.ckan_url = app.config['CKAN_URL']
    
    def cria_dataset(self, params : dict):

        url = self.ckan_url + 'package_create'

        params['name'] = unidecode.unidecode(params.get("name").lower().replace(" ", "_"))

        resposta = requests.post(url, headers = self.header, json = params)

        if resposta.json()['success'] == True:
            imprime_verde(f"Dataset {params['name']} criado com sucesso. \n")
        else:
            imprime_vermelho(f"Erro ao criar o dataset {params.get('name')}")
            imprime_vermelho(resposta.json())

        return resposta.json()
    
    def cria_recurso(self, params : dict, arquivo):

        url = self.ckan_url + 'resource_create'

        # Cada recurso tem uma foto, enviada através de form-data de acordo com a documentação

        resposta = requests.post(url, headers = self.header, data = params, files = arquivo)

        if resposta.json()['success'] == True:
            imprime_verde(f"Recurso {params['name']} criado com sucesso. \n")
        else:
            imprime_vermelho(f"Erro ao criar recurso {params['name']}")
            imprime_vermelho(resposta.json())

        return resposta.json()

def carregar_artista(nome_artista):

    artista = Artista()

    artista.inicializa_artista(nome_artista)

    return artista

def cria_dataset_artista(artista : Artista, id_organizacao, nome_grupo, requisicoes : Requisicoes):

    extras = [
        {"key" : "first_name", "value" : artista.nome},
        {"key" : "last_name", "value" : artista.sobrenome},
        {"key" : "gender" , "value" : artista.genero},
        {"key" : "birthday" , "value" : artista.data_nascimento},
        {"key" : "homepage" , "value" : artista.pagina},
        {"key" : "modified" , "value" : artista.atualizacao},
        {"key" : "links" , "value" : ",".join([link for link in artista.links])}
    ]

    params = {
        "name"  : f"{artista.nome.lower()}_{artista.sobrenome.lower().replace(' ', '')}",
        "title" : f"{artista.nome} {artista.sobrenome}",
        "maintainer" : artista.pesquisante,
        "maintainer_email" : artista.email_pesquisante,
        "notes" : artista.descricao,
        "tags" : [{"name" : nome} for nome in artista.palavras_chave],
        "groups" : [{"name" : nome_grupo}],
        "owner_org" : id_organizacao,
        "extras" : extras
    }

    return requisicoes.cria_dataset(params)

def cria_recurso_dataset(id_dataset, artista : Artista, imagem : str, requisicoes : Requisicoes, arquivos):

    params_recurso = {
        "package_id" : id_dataset
    }

    params_recurso['description'] = artista.imagens[imagem]['descricao']

    if artista.imagens[imagem].get('area') != None:

        params_recurso['hasArea'] = artista.imagens[imagem].get('area')

    elif artista.imagens[imagem].get('comprimento') != None:

        params_recurso['hasMetricLength'] = artista.imagens[imagem].get('comprimento')

    if artista.imagens[imagem].get('ano') != None:

        params_recurso['issued'] = artista.imagens[imagem].get('ano')

    if artista.imagens[imagem].get('fonte') != None:

        params_recurso['documentation'] = artista.imagens[imagem].get('fonte')

    if artista.imagens[imagem].get('titulo') != None:

        params_recurso['name'] = artista.imagens[imagem].get('titulo')
    
    else:

        params_recurso['name'] = imagem

    nome_arquivo = artista.imagens[imagem].get('nome_arquivo')
    arq = arquivos.get(nome_arquivo)

    arquivo = {
        'upload': (arq.filename, arq.stream, arq.mimetype)
    }
    
    return requisicoes.cria_recurso(params_recurso, arquivo)


def cria_artista_recursos_ckan(form, arquivos):

    requisicoes = Requisicoes(app.config['TOKEN_REQUISICOES'])

    artista = Artista(form, arquivos)

    resposta = cria_dataset_artista(artista, 'cap_ufrj', 'cap_ufrj', requisicoes)

    id_dataset = resposta['result']['id']

    for imagem in artista.imagens:

        cria_recurso_dataset(id_dataset, artista, imagem, requisicoes, arquivos)