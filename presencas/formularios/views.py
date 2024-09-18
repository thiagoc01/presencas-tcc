from flask import Blueprint, render_template, request
from flask_login import login_required
from .formulario_criacao import FormularioArtista
from .formulario_recursos import FormularioRecursos
from werkzeug.datastructures import ImmutableOrderedMultiDict
from .validador import ValidadorCriacaoArtista, ValidadorCriacaoObras
from .criador import cria_artista_recursos_ckan, cria_recursos_ckan
from presencas import app

formulario_blueprint = Blueprint("formulario", __name__)

@formulario_blueprint.route('/formulario_criacao/', methods=['GET', 'POST'])
@login_required
def index_formulario_criacao_artista():

    request.parameter_storage_class = ImmutableOrderedMultiDict

    form = FormularioArtista(request.form)

    form.erros = dict()

    if request.method == "POST":
        validador = ValidadorCriacaoArtista()
        if validador.realiza_validacao_form_artista(form, request.files) == 1:   # Essa validação permite colocar as mensagens de erro no formulário
            return render_template('formularios/formulario.html', form = form)

        if form.validate_on_submit():

            respostas, ocorreu_erro = cria_artista_recursos_ckan(form, request.files)

            return render_template('formularios/log_ckan.html', respostas = respostas, ocorreu_erro = ocorreu_erro)

    return render_template('formularios/formulario.html', form = form)

@formulario_blueprint.route('/formulario_adicao_obras_artista/', methods=['GET', 'POST'])
@login_required
def index_formulario_adicao_obras_artista():

    request.parameter_storage_class = ImmutableOrderedMultiDict

    form = FormularioRecursos(request.form)

    form.erros = dict()

    if request.method == "POST":

        validador = ValidadorCriacaoObras(app.config["TOKEN_REQUISICOES"])
        nome, erro = validador.realiza_validacao_form_artista(form, request.files)

        if erro == 1:
            return render_template('formularios/formulario_recursos.html', form = form)
        
        if form.validate_on_submit():

            respostas, ocorreu_erro = cria_recursos_ckan(form, request.files, nome)

            return render_template('formularios/log_ckan.html', respostas = respostas, ocorreu_erro = ocorreu_erro)

    return render_template('formularios/formulario_recursos.html', form = form)