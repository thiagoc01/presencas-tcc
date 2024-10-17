from flask_wtf import FlaskForm
from wtforms.fields import StringField, FieldList, FormField
from wtforms.validators import InputRequired
from wtforms.widgets import TableWidget
from .formulario_criacao import ImagensArtista

class FormularioRecursos(FlaskForm):

    class Meta:
        csrf = True

    nome = StringField('', [InputRequired("Insira o nome")], render_kw=dict(placeholder=""))

    imagens = FieldList(FormField(ImagensArtista, label=''), label = "", widget=TableWidget(), min_entries=1, max_entries=12)