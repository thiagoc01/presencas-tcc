from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired

class FormularioLogin(FlaskForm):

    class Meta:
        csrf = True

    usuario = StringField('Usuário', [InputRequired("Insira o usuário para login")], render_kw=dict(placeholder="Usuario"))
    senha = PasswordField('Senha', [InputRequired("Insira a senha para login")], render_kw=dict(placeholder="Senha"))
    lembrar_me = BooleanField('Permanecer conectado', default=False)

    def validate(self, extra_validators):
        validacao_form = super(FormularioLogin, self).validate()
        if not validacao_form:
            if self.usuario.data == "":
                self.erros["usuario"] = "- Insira um nome de usuário"

            if self.senha.data == "":
                self.erros["senha"] = "- Insira a senha"
            return False
        return True