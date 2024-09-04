from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, StringField, URLField, FieldList, FormField, BooleanField
from wtforms.validators import InputRequired, Length
from wtforms.widgets import TableWidget

class UrlsArtista(FlaskForm):

    titulo_url = StringField('Título da URL', [Length(max = 128), InputRequired("É necessário inserir o link")])

    url = URLField('URL', [InputRequired("É necessário inserir o link")])

    remover_link = BooleanField('', render_kw=dict(type='button', value='Remover link'))

class FormularioArtista(FlaskForm):

    class Meta:
        csrf = True

    nome = StringField('Nome')

    trajetoria = TextAreaField('Trajetória', [InputRequired("É necessária a trajetória")])

    producao = TextAreaField('Produção', [InputRequired("É necessária a produção")])

    links = FieldList(FormField(UrlsArtista, label=''), label = "", widget=TableWidget(), min_entries=1, max_entries=8)






