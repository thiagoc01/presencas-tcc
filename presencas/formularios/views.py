from flask import Blueprint, render_template, request, session, make_response, abort
from flask_login import login_required
from .formulario_criacao import FormularioArtista
from .formulario_recursos import FormularioRecursos
from werkzeug.datastructures import ImmutableOrderedMultiDict
from .validador import ValidadorCriacaoArtista, ValidadorCriacaoObras
from .criador import cria_artista_recursos_ckan, cria_recursos_ckan
from .solicitacao import Solicitacao
from presencas import app, db

formulario_blueprint = Blueprint("formulario", __name__)

@formulario_blueprint.route('/api/obter_progresso/<id>', methods=['GET'])
@login_required
def retornar_progresso(id):

    if not id:
        abort(400)

    try:
        progresso = db.session.execute(db.select(Solicitacao).filter_by(sessao = session.get('_id'), id = id)).first()
    except Exception:
        abort(500)

    if progresso:
        return make_response(str(progresso[0].progresso)), 200

    else:
        abort(400)

@formulario_blueprint.route('/formulario_criacao/', methods=['GET', 'POST'])
@login_required
def index_formulario_criacao_artista():

    request.parameter_storage_class = ImmutableOrderedMultiDict

    form = FormularioArtista(request.form)

    form.erros = dict()

    if request.method == "POST":

        if request.values.get('id_solicitacao') == None:
            abort(400)

        validador = ValidadorCriacaoArtista()
        if validador.realiza_validacao_form_artista(form, request.files) == 1:   # Essa validação permite colocar as mensagens de erro no formulário
            return render_template('formularios/formulario.html', form = form)

        if form.validate_on_submit():

            respostas, ocorreu_erro, codigo = cria_artista_recursos_ckan(form, request.files, request.values.get('id_solicitacao'))

            return render_template('formularios/log_ckan.html', respostas = respostas, ocorreu_erro = ocorreu_erro, esta_criando_artista = True)

    return render_template('formularios/formulario.html', form = form)

@formulario_blueprint.route('/formulario_adicao_obras_artista/', methods=['GET', 'POST'])
@login_required
def index_formulario_adicao_obras_artista():

    request.parameter_storage_class = ImmutableOrderedMultiDict

    form = FormularioRecursos(request.form)

    form.erros = dict()

    if request.method == "POST":

        if request.values.get('id_solicitacao') == None:
            abort(400)

        validador = ValidadorCriacaoObras(app.config["TOKEN_REQUISICOES"])
        nome, erro = validador.realiza_validacao_form_artista(form, request.files)

        if erro == 1:
            return render_template('formularios/formulario_recursos.html', form = form)
        
        if form.validate_on_submit():

            respostas, ocorreu_erro, codigo = cria_recursos_ckan(form, request.files, nome, request.values.get('id_solicitacao'))

            return render_template('formularios/log_ckan.html', respostas = respostas, ocorreu_erro = ocorreu_erro, esta_criando_artista = False)

    return render_template('formularios/formulario_recursos.html', form = form)