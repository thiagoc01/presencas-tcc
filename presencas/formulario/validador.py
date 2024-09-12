def retorna_mensagem_erro_form(form, nome_campo, campo, mensagem):
    if campo.data == None or campo.data == '':
        form.erros[nome_campo] = mensagem

def retorna_mensagem_erro_campo_composto_form(form, campo_form, num_campo, nome_campo, campo, mensagem):
    if campo.data == None or campo.data == '':
        form.erros[campo_form][num_campo][nome_campo] = mensagem

def realiza_validacao_form_artista(form, arquivos):

    retorna_mensagem_erro_form(form, "nome", form.nome, "- É necessário inserir um nome")

    retorna_mensagem_erro_form(form, "trajetoria", form.trajetoria, "- É necessário inserir a trajetória")

    retorna_mensagem_erro_form(form, "producao", form.producao, "- É necessário inserir a produção")

    form.erros['imagens'] = [dict() for _ in range(0, form.imagens.__len__())]
    form.erros['links'] = [dict() for _ in range(0, form.links.__len__())]
    form.erros['palavras_chave'] = [dict() for _ in range(0, form.palavras_chave.__len__())] 

    i = 0

    for campo in form.imagens:
        retorna_mensagem_erro_campo_composto_form(form, "imagens", i, "fonte",  campo.fonte, "- É necessário inserir uma URL")

        i += 1

    i = 0

    if len(arquivos.to_dict().items()) != 0:
        for _, arquivo in arquivos.to_dict().items():
            if arquivo.filename == '':
                form.erros['imagens'][i]['arquivo'] = "- É necessário inserir um arquivo .jpg, .jpeg, .jfif ou .png"
            i += 1

    i = 0

    for campo in form.links:
        retorna_mensagem_erro_campo_composto_form(form, "links", i, "titulo_url",  campo.titulo_url, "- É necessário inserir um título para a URL")
        retorna_mensagem_erro_campo_composto_form(form, "links", i, "url",  campo.url, "- É necessário inserir uma URL")
        i += 1

    i = 0

    for campo in form.palavras_chave:
        retorna_mensagem_erro_campo_composto_form(form, "palavras_chave", i, "palavra_chave",  campo.palavra_chave, "- É necessário inserir a palavra-chave")
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