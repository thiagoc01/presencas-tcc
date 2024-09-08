from flask import Blueprint, render_template, request, flash
from .formulario import FormularioArtista
from werkzeug.datastructures import ImmutableOrderedMultiDict

formulario_blueprint = Blueprint("formulario", __name__)


@formulario_blueprint.route('/formulario', methods=['GET', 'POST'])
def index():

    request.parameter_storage_class = ImmutableOrderedMultiDict
    form = FormularioArtista(request.form)
    form.erros = dict()
    form.erros['links']= [{'titulo_url' : 'Erro1', 'url' : 'Erro2'}, {'titulo_url' : 'Erro3', 'url' : 'Erro4'}]
    form.erros['imagens']= [{'titulo' : 'Erro1', 'material' : 'Erro2'}, {'titulo' : 'Erro3', 'material' : 'Erro4'}]
    
    if form.validate_on_submit() and request.method == "POST":
        print(request.form)
        
        for i in form.links.data:
            print(i)
    return render_template('formulario/formulario.html', form=  form)