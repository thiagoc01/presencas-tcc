from flask import Blueprint, render_template, request
from .formulario import FormularioArtista
from werkzeug.datastructures import ImmutableOrderedMultiDict
from .validador import realiza_validacao_form_artista

formulario_blueprint = Blueprint("formulario", __name__)


@formulario_blueprint.route('/formulario', methods=['GET', 'POST'])
def index():

    request.parameter_storage_class = ImmutableOrderedMultiDict

    form = FormularioArtista(request.form)

    form.erros = dict()

    if request.method == "POST":
        if realiza_validacao_form_artista(form, request.files) == 1:   # Essa validação permite colocar as mensagens de erro no formulário
            return render_template('formulario/formulario.html', form = form)
    
        if form.validate_on_submit():

            print(request.form)
            print(request.files)

            for i in form.links.data:
                print(i)

            for i in form.palavras_chave.data:
                print(i)

    return render_template('formulario/formulario.html', form = form)