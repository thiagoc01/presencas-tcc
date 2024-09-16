from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, StringField, URLField, FieldList, FormField, Field, DateField, FileField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError, URL, Email
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

    def ajusta_dia(dia):

        if dia is not None and dia.isoformat() == '1900-01-01':

            return date.today()

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

    titulo = StringField("Titulo", [Length(max = 128)], render_kw=dict(placeholder="Título da imagem (se não houver, deixe em branco)"))

    material = StringField("Material", [Length(max = 128)], render_kw=dict(placeholder="Material da obra (se não houver, deixe em branco)"))

    tamanho = StringField("Tamanho", [Length(max = 128)], render_kw=dict(placeholder="Tamanho em centímetros ou área física (se não houver, deixe em branco)"))

    data = StringField("Data da criação da obra", [Length(max = 128)], render_kw=dict(placeholder="Ano ou mês/ano ou dia/mês/ano"))

    descricao = TextAreaField('Descrição', render_kw=dict(placeholder="Digite a descrição aqui"))

    outras_infos = TextAreaField('Outras informações da imagem', render_kw=dict(placeholder="Digite outras informações da imagem, se necessário, como série etc."))

    fonte = URLField('URL',render_kw=dict(placeholder="http://", \
                                        oninvalid="setCustomValidity('Insira uma URL válida')", \
                                        oninput="setCustomValidity('')"))
    
    arquivo = FileField('Arquivo', render_kw=dict(required=True, oninput="setCustomValidity('')", \
                                    oninvalid="setCustomValidity('Insira um arquivo .jpg, .jpeg, .jfif ou .png')"))
    
    remover_campo_imagem = Field(widget=gera_botao_sem_acao, label='', render_kw=dict(conteudo="Remover campo"))


class UrlsArtista(FlaskForm):

    url = URLField('URL', [InputRequired("É necessário inserir o link"), \
                URL(require_tld=False, message="Insira uma URL válida")], render_kw=dict(placeholder="http://", \
                                                                                        oninvalid="setCustomValidity('Insira uma URL válida')", \
                                                                                        oninput="setCustomValidity('')"))

    remover_campo_link = Field(widget=gera_botao_sem_acao, label='', render_kw=dict(conteudo="Remover link"))

class PalavrasChave(FlaskForm):

    palavra_chave = StringField('', [InputRequired('É necessário inserir a palavra-chave')], render_kw=dict(placeholder='Palavra-chave'))

    remover_campo_palavras_chave = Field(widget=gera_botao_sem_acao, label='', render_kw=dict(conteudo="Remover campo"))

class FormularioArtista(FlaskForm):

    class Meta:
        csrf = True

    nome = StringField('Nome', [InputRequired("Insira o nome")], render_kw=dict(placeholder="Nome"))

    trajetoria = TextAreaField('Trajetória', [InputRequired("É necessária a trajetória")], render_kw=dict(placeholder="Digite a trajetória aqui"))

    producao = TextAreaField('Produção', [InputRequired("É necessária a produção")], render_kw=dict(placeholder="Digite a produção aqui"))

    imagens = FieldList(FormField(ImagensArtista, label=''), label = "", widget=TableWidget(), min_entries=1, max_entries=12)

    links = FieldList(FormField(UrlsArtista, label=''), label = "", widget=TableWidget(), min_entries=1, max_entries=8)

    pesquisante = StringField('Pesquisante', render_kw=dict(placeholder="Pesquisante"))

    email_pesquisante = StringField('E-mail pesquisante', [Email("Digite um e-mail válido")], render_kw=dict(placeholder="E-mail"))

    data_nascimento = StringField("Data de nascimento", [Length(max = 128)], render_kw=dict(placeholder="Ano ou mês/ano ou dia/mês/ano"))

    palavras_chave = FieldList(FormField(PalavrasChave, label = ''), label = "", widget=TableWidget(), min_entries=1, max_entries=12)

    genero = StringField("Gênero", render_kw=dict(placeholder="Gênero"))

    pagina = URLField('URL', [URL(require_tld=False, message="Insira uma URL válida")], render_kw=dict(placeholder="http://", \
                                                                                        oninvalid="setCustomValidity('Insira uma URL válida')", \
                                                                                        oninput="setCustomValidity('')"))

    ultima_atualizacao = DateField('Data da última atualização', format = ['%d/%m/%Y', '%Y-%m-%d', ''], \
                                filters=[DataValida.ajusta_dia], \
                                render_kw=dict(max=date.today(), \
                                oninvalid=f'setCustomValidity("Selecione um valor que não seja depois de {date.strftime(date.today(), "%d/%m/%Y")}")', \
                                oninput='setCustomValidity("")'), validators=[DataValida()])