from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, StringField, URLField, FieldList, FormField, Field, DateField, FileField
from wtforms.validators import InputRequired, Length, ValidationError
from wtforms.widgets import TableWidget, html_params
from datetime import date

def gera_botao_sem_acao(field, **kwargs):
    kwargs.setdefault('type', 'button')
    conteudo = kwargs.pop('conteudo', '')
    id = kwargs.pop('id', field.id)
    html = '<button %s ' % html_params(id=id)
    options = dict(kwargs, name=field.name)
    html += html_params(**options)
    html += '>%s</button>' % conteudo
    return html

class DataValida(object):
    def __init__(self, mensagem=None):
        if not mensagem:
            mensagem = 'Insira uma data válida e que não esteja no futuro'
        self.mensagem = mensagem

    def __call__(self, form, field):
        if date.today() < date.fromisoformat(date.strftime(field.data, "%Y-%m-%d")):
            raise ValidationError(self.mensagem)
        
class ImagensArtista(FlaskForm):

    titulo = StringField("Titulo", [Length(max = 128)])
    material = StringField("Material", [Length(max = 128)])
    tamanho = StringField("Tamanho", [Length(max = 128)])
    data = StringField("Titulo", [Length(max = 128)])
    descricao = TextAreaField('Descrição')
    fonte = URLField('URL')
    arquivo = FileField('Arquivo', render_kw=dict(required=True, oninvalid='setCustomValidity("Insira um arquivo")'))
    remover_campo_imagem = Field(widget=gera_botao_sem_acao, label='', render_kw=dict(conteudo="Remover campo"))


class UrlsArtista(FlaskForm):

    titulo_url = StringField('Título da URL', [Length(max = 128), InputRequired("É necessário inserir o link")])

    url = URLField('URL', [InputRequired("É necessário inserir o link")])

    remover_campo_link = Field(widget=gera_botao_sem_acao, label='', render_kw=dict(conteudo="Remover link"))

class FormularioArtista(FlaskForm):

    class Meta:
        csrf = True

    nome = StringField('Nome')

    trajetoria = TextAreaField('Trajetória', [InputRequired("É necessária a trajetória")])

    producao = TextAreaField('Produção', [InputRequired("É necessária a produção")])

    imagens = FieldList(FormField(ImagensArtista, label=''), label = "", widget=TableWidget(), min_entries=1, max_entries=12)

    links = FieldList(FormField(UrlsArtista, label=''), label = "", widget=TableWidget(), min_entries=1, max_entries=8)

    ultima_atualizacao = DateField('Data da última atualização', format = ['%d/%m/%Y', '%Y-%m-%d'], \
                                render_kw=dict(max=date.today(), \
                                oninvalid=f'setCustomValidity("Selecione um valor que não seja depois de {date.strftime(date.today(), "%d/%m/%Y")}")'), \
                                validators=[DataValida()])