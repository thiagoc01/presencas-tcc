from flask import Blueprint, render_template, request, flash
from .formulario import FormularioArtista

formulario_blueprint = Blueprint("formulario", __name__)

@formulario_blueprint.route('/formulario', methods=['GET', 'POST'])
def index():

    form = FormularioArtista(request.form)
    
    if form.validate_on_submit() and request.method == "POST":
        print(request.form)
        
        for i in form.links.data:
            print(i)
    return render_template('formulario/formulario.html', form=  form)