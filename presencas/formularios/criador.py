import unidecode
import requests
import re
from flask import abort
from presencas import app, db
from datetime import date
import jsbeautifier
from .solicitacao import Solicitacao
from flask_login import current_user
import time
from logging import SUCCESS

def adiciona_solicitacao(solicitacao):
    try:
        db.session.add(solicitacao)
        db.session.commit()
    except Exception as e:
        abort(500, description = e)

def atualiza_progresso(solicitacao, progresso, TOTAL):
    try:
        solicitacao.progresso = progresso / TOTAL
        db.session.commit()
    except Exception:
        pass

def deleta_solicitacao(solicitacao):
    try:
        db.session.delete(solicitacao)
        db.session.commit()
    except Exception:
        pass

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

        if len(arquivos.to_dict().items()) != 0:

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

                    eArea = re.compile(r"[0-9\,]{1,5} *[xX] *[0-9\,]{1,5} *(cm)?")
                    eComprimento = re.compile(r"[0-9]{1,3}(?= *cm)")

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

        if form.trajetoria.data:

            self.descricao = f"**Trajetória**\n<br>\n {form.trajetoria.data}"

        if form.producao.data:
            self.descricao += f"\n<br>\n**Produção**\n<br>\n {form.producao.data}"

        for campo in form.links:

            self.links.append(campo.url.data)

        if form.ultima_atualizacao.data:

            self.atualizacao = date.strftime(form.ultima_atualizacao.data, "%d/%m/%Y")

        if form.genero.data:

            self.genero = form.genero.data

        if form.data_nascimento.data:

            self.data_nascimento = form.data_nascimento.data

        if form.email_pesquisante.data != None:

            self.email_pesquisante = form.email_pesquisante.data

        if form.pesquisante.data != None:

            self.pesquisante = form.pesquisante.data

        if form.pagina.data:

            self.pagina = form.pagina.data

        for palavra_chave in form.palavras_chave:

            self.palavras_chave.append(palavra_chave.palavra_chave.data)

class ArtistaImagens(Artista):

    def __init__(self, form, arquivos):

        self.nome = ""
        self.sobrenome = ""
        self.nome_completo = ""
        self.imagens = {}

        self._inicializa_artista(form, arquivos)

    def _inicializa_artista(self, form, arquivos):

        nome = self.nome_completo = form.nome.data

        if len(nome.split(" ")) == 2:
            self.nome, self.sobrenome = nome.split(" ")
        else:
            self.nome, self.sobrenome = nome.split(" ")[0], " ".join(nome.split()[1:])

        self._carrega_imagens(form, arquivos)

class Requisicoes:
    def __init__(self, token : str, solicitacao : Solicitacao):
        self.header = {"Authorization" : token}
        self.ckan_url = app.config['CKAN_URL']
        self.solicitacao = solicitacao
    
    def cria_dataset(self, params : dict):

        ocorreu_erro = False

        url = self.ckan_url + 'package_create'

        params['name'] = unidecode.unidecode(params.get("name").lower().replace(" ", "_"))

        try:

            resposta = requests.post(url, headers = self.header, json = params)

        except requests.exceptions.ConnectionError:
            app.logger.error(f"{current_user.usuario} | Erro ao criar o dataset {params.get('name')}")
            deleta_solicitacao(self.solicitacao)
            abort(502)

        if resposta.json()['success'] == True:
            app.logger.log(SUCCESS, f"{current_user.usuario} | Dataset {params['name']} criado com sucesso.")
        else:
            app.logger.error(f"{current_user.usuario} | Erro ao criar o dataset {params.get('name')}")
            app.logger.error(resposta.json())
            ocorreu_erro = True

        return resposta.json(), ocorreu_erro, resposta.status_code
    
    def cria_recurso(self, params : dict, arquivo):

        ocorreu_erro = False

        url = self.ckan_url + 'resource_create'

        # Cada recurso tem uma foto, enviada através de form-data de acordo com a documentação

        try:

            resposta = requests.post(url, headers = self.header, data = params, files = arquivo)

        except requests.exceptions.ConnectionError:
            app.logger.error(f"{current_user.usuario} | Erro ao criar o dataset {params.get('name')}")
            deleta_solicitacao(self.solicitacao)
            abort(502)

        if resposta.json()['success'] == True:
            app.logger.log(SUCCESS, f"{current_user.usuario} | Recurso {params['name']} criado com sucesso.")
        else:
            app.logger.error(f"{current_user.usuario} | Erro ao criar recurso {params['name']}")
            app.logger.error(resposta.json())
            ocorreu_erro = True

        return resposta.json(), ocorreu_erro, resposta.status_code

def cria_dataset_artista(artista : Artista, id_organizacao, nome_grupo, requisicoes : Requisicoes):

    extras = []

    extras.append({"key" : "first_name", "value" : artista.nome}) if artista.nome else ""
    extras.append({"key" : "last_name", "value" : artista.sobrenome}) if artista.sobrenome else ""
    extras.append({"key" : "gender" , "value" : artista.genero}) if artista.genero else ""
    extras.append({"key" : "birthday" , "value" : artista.data_nascimento}) if artista.data_nascimento else ""
    extras.append({"key" : "homepage" , "value" : artista.pagina}) if artista.pagina else ""
    extras.append({"key" : "modified" , "value" : artista.atualizacao}) if artista.atualizacao else ""

    if artista.links and artista.links[0] != None:
        extras.append({"key" : "links" , "value" : ",".join([link for link in artista.links])})

    params = {
        "name"  : f"{artista.nome.lower()}_{artista.sobrenome.lower().replace(' ', '')}",
        "title" : f"{artista.nome} {artista.sobrenome}",
        "notes" : artista.descricao,
        "groups" : [{"name" : nome_grupo}],
        "owner_org" : id_organizacao,
        "extras" : extras
    }

    if artista.pesquisante != "":
        params['maintainer'] = artista.pesquisante

    if artista.email_pesquisante != "":
        params['maintainer_email'] = artista.email_pesquisante

    if artista.palavras_chave and artista.palavras_chave[0] != None:
        params["tags"] = [{"name" : nome} for nome in artista.palavras_chave]

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


def cria_artista_recursos_ckan(form, arquivos, id_solicitacao):

    solicitacao = Solicitacao(id = id_solicitacao)

    requisicoes = Requisicoes(app.config['TOKEN_REQUISICOES'], solicitacao)
    respostas = []

    progresso = 1

    artista = Artista(form, arquivos)

    TOTAL = 1 + len(artista.imagens)

    adiciona_solicitacao(solicitacao)

    resposta, erro, codigo_resposta = cria_dataset_artista(artista, 'cap_ufrj', 'cap_ufrj', requisicoes)

    atualiza_progresso(solicitacao, progresso, TOTAL)

    progresso += 1

    respostas.append(jsbeautifier.beautify(str(resposta)))

    if erro:
        deleta_solicitacao(solicitacao)
        return respostas, True, codigo_resposta

    id_dataset = resposta['result']['id']

    for imagem in artista.imagens:

        resposta, erro, codigo_resposta = cria_recurso_dataset(id_dataset, artista, imagem, requisicoes, arquivos)
        respostas.append(jsbeautifier.beautify(str(resposta)))

        if erro:
            deleta_solicitacao(solicitacao)
            return respostas, True, codigo_resposta
        
        atualiza_progresso(solicitacao, progresso, TOTAL)

        progresso += 1

    time.sleep(2)

    deleta_solicitacao(solicitacao)

    return respostas, False, 201

def cria_recursos_ckan(form, arquivos, nome_artista, id_solicitacao):

    solicitacao = Solicitacao(id = id_solicitacao)

    requisicoes = Requisicoes(app.config['TOKEN_REQUISICOES'], solicitacao)
    respostas = []

    artista = ArtistaImagens(form, arquivos)

    progresso = 1

    TOTAL = len(artista.imagens)

    adiciona_solicitacao(solicitacao)

    for imagem in artista.imagens:

        resposta, erro, codigo_resposta = cria_recurso_dataset(nome_artista, artista, imagem, requisicoes, arquivos)
        respostas.append(jsbeautifier.beautify(str(resposta)))

        if erro:
            deleta_solicitacao(solicitacao)
            return respostas, True, codigo_resposta

        atualiza_progresso(solicitacao, progresso, TOTAL)

        progresso += 1

    deleta_solicitacao(solicitacao)

    return respostas, False, 201