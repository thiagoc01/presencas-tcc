from .criador import Requisicoes
import requests, unidecode
from presencas import app

class ValidadorCriacaoArtista():

    def retorna_mensagem_erro_form(self, form, nome_campo, campo, mensagem):
        if campo.data == None or campo.data == '':
            form.erros[nome_campo] = mensagem

    def retorna_mensagem_erro_campo_composto_form(self, form, campo_form, num_campo, nome_campo, campo, mensagem):
        if campo.data == None or campo.data == '':
            form.erros[campo_form][num_campo][nome_campo] = mensagem

    def realiza_validacao_form_artista(self, form, arquivos):

        self.retorna_mensagem_erro_form(form, "nome", form.nome, "- É necessário inserir um nome")

        if form.erros.get('nome') == None:
            if len(form.nome.data.split(" ")) == 2:
                nome, sobrenome = form.nome.data.split(" ")
            else:
                nome, sobrenome = form.nome.data.split(" ")[0], " ".join(form.nome.data.split()[1:])

            nome = f"{nome.lower()}_{sobrenome.lower().replace(' ', '')}"

            nome = unidecode.unidecode(nome)

            if VerificadorExistenciaArtista(app.config["TOKEN_REQUISICOES"]).verifica_artista(nome):
                form.erros['nome'] = "Artista já cadastrado"

        self.retorna_mensagem_erro_form(form, "trajetoria", form.trajetoria, "- É necessário inserir a trajetória")

        self.retorna_mensagem_erro_form(form, "producao", form.producao, "- É necessário inserir a produção")

        form.erros['imagens'] = [dict() for _ in range(0, form.imagens.__len__())]
        form.erros['links'] = [dict() for _ in range(0, form.links.__len__())]
        form.erros['palavras_chave'] = [dict() for _ in range(0, form.palavras_chave.__len__())]

        i = 0

        if len(arquivos.to_dict().items()) != 0:
            for _, arquivo in arquivos.to_dict().items():
                if arquivo.filename == '':
                    form.erros['imagens'][i]['arquivo'] = "É necessário inserir um arquivo .jpg, .jpeg, .jfif ou .png"
                i += 1

        i = 0

        for campo in form.links:
            self.retorna_mensagem_erro_campo_composto_form(form, "links", i, "url",  campo.url, "É necessário inserir uma URL")
            i += 1

        i = 0

        for campo in form.palavras_chave:
            self.retorna_mensagem_erro_campo_composto_form(form, "palavras_chave", i, "palavra_chave",  campo.palavra_chave, "É necessário inserir a palavra-chave")
            i += 1

        # A validação da data é feita no módulo do formulário

        # Retorna 1 se houve erro

        for campo, erros in form.erros.items():
            if campo != 'imagens' and campo != 'links' and campo != 'palavras_chave' and erros != None:
                return 1
            elif campo == 'imagens' or campo == 'links' or campo == 'palavras_chave':
                for sub_campo in erros:
                    if len(sub_campo.items()) > 0:
                        return 1

        return 0

class VerificadorExistenciaArtista(Requisicoes):

    def __init__(self, token):

        super().__init__(token)

    def verifica_artista(self, nome : str):

        url = self.ckan_url + 'package_list'

        artistas = requests.get(url, headers = self.header, data = {}).json()['result']

        try:
            artistas.index(nome)
            return True

        except ValueError:
            return False


class ValidadorCriacaoObras(ValidadorCriacaoArtista):

    def __init__(self, token):

        self.verificador = VerificadorExistenciaArtista(token)

    def realiza_validacao_form_artista(self, form, arquivos):

        nome = None

        self.retorna_mensagem_erro_form(form, "nome", form.nome, "É necessário inserir um nome")

        if form.erros.get('nome') == None:

            if len(form.nome.data.split(" ")) == 2:
                nome, sobrenome = form.nome.data.split(" ")
            else:
                nome, sobrenome = form.nome.data.split(" ")[0], " ".join(form.nome.data.split()[1:])

            nome = f"{nome.lower()}_{sobrenome.lower().replace(' ', '')}"

            nome = unidecode.unidecode(nome)

            if not self.verificador.verifica_artista(nome):
                form.erros['nome'] = "É necessário inserir um nome de um artista cadastrado"

        form.erros['imagens'] = [dict() for _ in range(0, form.imagens.__len__())]

        i = 0

        if len(arquivos.to_dict().items()) == 0:
            form.erros['imagens'][i]['arquivo'] = "É necessário inserir um arquivo .jpg, .jpeg, .jfif ou .png"
            return nome, 1

        for _, arquivo in arquivos.to_dict().items():
            if arquivo.filename == '':
                form.erros['imagens'][i]['arquivo'] = "É necessário inserir um arquivo .jpg, .jpeg, .jfif ou .png"
            i += 1

        # Retorna 1 se houve erro

        for campo, erros in form.erros.items():
            if campo != 'imagens' and erros != None:
                return nome, 1
            elif campo == 'imagens':
                for sub_campo in erros:
                    if len(sub_campo.items()) > 0:
                        return nome, 1

        return nome, 0