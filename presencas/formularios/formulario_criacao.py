from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, StringField, URLField, FieldList, FormField, Field, DateField, FileField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError
from wtforms.widgets import TableWidget, html_params
from datetime import date
from dateutil.parser import parse
from jinja2.filters import do_mark_safe

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

    def ajusta_dia(dia):

        if dia is not None and dia.isoformat() == '1900-01-01':

            return date.today()

        elif dia is not None:

            return dia

    def __call__(self, form, field):

        if field.data:
            try:
                if date.today() < date.fromisoformat(date.strftime(field.data, "%Y-%m-%d")):
                    form.erros['ultima_atualizacao'] = "Insira uma data válida e anterior ou igual a de hoje"
                    raise ValidationError(self.mensagem)
            except:
                form.erros['ultima_atualizacao'] = "Insira uma data válida e anterior ou igual a de hoje"
                raise ValidationError(self.mensagem)
            
        
class ImagensArtista(FlaskForm):

    class Meta:
        csrf = False

    titulo = StringField("", [Length(max = 128)],
                        render_kw=dict(placeholder="Título da imagem (se houver)"))

    tecnica = StringField("", [Length(max = 128)],
                           render_kw=dict(placeholder="Técnica da obra (se houver)"))

    tamanho = StringField("", [Length(max = 128)],
                          render_kw=dict(placeholder="Tamanho em centímetros ou área física (se houver)"))

    data = StringField("", [Length(max = 128)],
                       render_kw=dict(placeholder="Ano ou mês/ano ou dia/mês/ano (se houver)"))

    descricao = TextAreaField('', render_kw=dict(placeholder=""))

    outras_infos = TextAreaField('',
                                render_kw=dict(placeholder="Se houver, digite outras informações da imagem, se necessário, como série etc."))

    fonte = URLField('', render_kw=dict(placeholder="http://", \
                                        oninvalid="setCustomValidity('Insira uma URL válida')", \
                                        oninput="setCustomValidity('')"))
    
    arquivo = FileField(do_mark_safe('<i class="fa-solid fa-upload"></i> Procurar...'), render_kw=dict(required=True, oninput="setCustomValidity('')", \
                                    oninvalid="setCustomValidity('Insira um arquivo .jpg, .jpeg, .jfif ou .png')",
                                    accept=".png, .jpeg, .jpg, .jfif"))
    
    remover_campo_imagem = Field(widget=gera_botao_sem_acao, label='', render_kw=dict(conteudo=do_mark_safe('<i class="fa-solid fa-xmark pe-2"></i>Remover campo')))


class UrlsArtista(FlaskForm):

    class Meta:
        csrf = False

    url = URLField('', render_kw=dict(required=True, \
                            placeholder="http://", \
                            oninvalid="setCustomValidity('Insira uma URL válida')", \
                            oninput="setCustomValidity('')"))

    remover_campo_link = Field(widget=gera_botao_sem_acao, label='', render_kw=dict(conteudo='<i class="fa-solid fa-xmark pe-2"></i>Remover link'))

class PalavrasChave(FlaskForm):

    class Meta:
        csrf = False

    palavra_chave = StringField('', render_kw=dict(placeholder='', required=True))

    remover_campo_palavras_chave = Field(widget=gera_botao_sem_acao, label='', render_kw=dict(conteudo='<i class="fa-solid fa-xmark pe-2"></i>Remover campo'))

class Linguagens(FlaskForm):

    class Meta:
        csrf = False

    linguagem = StringField('', render_kw=dict(placeholder='', required=True))

    remover_campo_linguagem = Field(widget=gera_botao_sem_acao, label='', render_kw=dict(conteudo='<i class="fa-solid fa-xmark pe-2"></i>Remover campo'))

class CidadeAtuacao(FlaskForm):

    class Meta:
        csrf = False

    cidade_atuacao = StringField('', render_kw=dict(placeholder='', required=True))

    remover_campo_cidade_atuacao = Field(widget=gera_botao_sem_acao, label='', render_kw=dict(conteudo='<i class="fa-solid fa-xmark pe-2"></i>Remover campo'))

class EstadoAtuacao(FlaskForm):

    class Meta:
        csrf = False

    estado_atuacao = StringField('', render_kw=dict(placeholder='', required=True))

    remover_campo_estado_atuacao = Field(widget=gera_botao_sem_acao, label='', render_kw=dict(conteudo='<i class="fa-solid fa-xmark pe-2"></i>Remover campo'))

class PaisAtuacao(FlaskForm):

    class Meta:
        csrf = False

    pais_atuacao = StringField('', render_kw=dict(placeholder='', required=True))

    remover_campo_pais_atuacao = Field(widget=gera_botao_sem_acao, label='', render_kw=dict(conteudo='<i class="fa-solid fa-xmark pe-2"></i>Remover campo'))

class FormularioArtista(FlaskForm):

    class Meta:
        csrf = True

    nome = StringField('', [InputRequired("Insira o nome")], render_kw=dict(placeholder=""))

    trajetoria = TextAreaField('', [InputRequired("É necessária a trajetória")], render_kw=dict(placeholder=""))

    producao = TextAreaField('', [InputRequired("É necessária a produção")], render_kw=dict(placeholder=""))

    imagens = FieldList(FormField(ImagensArtista, label=''), label = "", widget=TableWidget(), min_entries=0, max_entries=12)

    links = FieldList(FormField(UrlsArtista, label=''), label = "", widget=TableWidget(), min_entries=0, max_entries=8)

    pesquisante = StringField('', render_kw=dict(placeholder=""))

    email_pesquisante = EmailField('', render_kw=dict(placeholder=""))

    quantidade = StringField('', render_kw=dict(placeholder=""))

    data_inicio = StringField("", [Length(max = 128)], render_kw=dict(placeholder="Ano ou mês/ano ou dia/mês/ano"))

    data_fim = StringField("", [Length(max = 128)], render_kw=dict(placeholder="Ano ou mês/ano ou dia/mês/ano"))

    palavras_chave = FieldList(FormField(PalavrasChave, label = ''), label = "", widget=TableWidget(), min_entries=0, max_entries=12)

    linguagem = FieldList(FormField(Linguagens, label = ''), label = "", widget=TableWidget(), min_entries=0, max_entries=12)

    cidade = StringField("", render_kw=dict(placeholder=""))

    estado = StringField("", render_kw=dict(placeholder=""))

    cidade_atuacao = FieldList(FormField(CidadeAtuacao, label = ''), label = "", widget=TableWidget(), min_entries=0, max_entries=4)

    estado_atuacao = FieldList(FormField(EstadoAtuacao, label = ''), label = "", widget=TableWidget(), min_entries=0, max_entries=4)

    pais_atuacao = FieldList(FormField(PaisAtuacao, label = ''), label = "", widget=TableWidget(), min_entries=0, max_entries=4)

    genero = StringField("", render_kw=dict(placeholder=""))

    pagina = URLField('', render_kw=dict(placeholder="http://", \
                            oninvalid="setCustomValidity('Insira uma URL válida')", \
                            oninput="setCustomValidity('')"))

    ultima_atualizacao = DateField('Data da última atualização', format = ['%d/%m/%Y', '%Y-%m-%d', ''], \
                                filters=[DataValida.ajusta_dia], \
                                render_kw=dict(max=date.today(), \
                                oninvalid=f'setCustomValidity("Selecione um valor que não seja depois de {date.strftime(date.today(), "%d/%m/%Y")}")', \
                                oninput='setCustomValidity("")'), validators=[DataValida()])