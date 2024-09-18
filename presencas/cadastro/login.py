from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired

class FormularioLogin(FlaskForm):

    class Meta:
        csrf = True

    usuario = StringField('Usuário', [InputRequired("Insira o usuário para login")], render_kw=dict(placeholder="Usuario"))
    senha = PasswordField('Senha', [InputRequired("Insira a senha para login")], render_kw=dict(placeholder="Senha"))
    lembrar_me = BooleanField('Permanecer conectado', default=False)