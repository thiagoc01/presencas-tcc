from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms.fields import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired
from .usuario import Usuario
from presencas import db
import re

class FormularioCadastro(FlaskForm):

    class Meta:
        csrf = True

    usuario = StringField('', [InputRequired("Insira o usuário para cadastro")], render_kw=dict(placeholder=""))
    senha = PasswordField('', [InputRequired("Insira a senha para cadastro")], render_kw=dict(placeholder=""))
    e_adm = BooleanField('', default=False)
    confirmar_senha = PasswordField('', [InputRequired("Insira a senha para confirmar")], render_kw=dict(placeholder="Digite a senha novamente"))

    def validate(self, extra_validators):
        validacao_form = super(FormularioCadastro, self).validate()
        if not validacao_form:
            if self.usuario.data == "":
                self.erros["usuario"] = "Digite um nome de usuário"
            if self.senha.data == "":
                self.erros["senha"] = "Digite uma senha"
            if self.confirmar_senha.data == "":
                self.erros["confirmar_senha"] = "Digite a confirmação da senha"
            return False
        usuario = db.session.execute(db.select(Usuario).filter_by(usuario = self.usuario.data)).first()
        if usuario:
            self.erros["usuario"] = "Usuário já existente"

        if self.senha.data != self.confirmar_senha.data:
            self.erros["confirmar_senha"] = "As senhas não coincidem"

        regex_simbolos = re.compile("[@_!#$%^&*()<>?/\|}{~:]")
        regex_minuscula = re.compile("[a-z]")
        regex_maiuscula = re.compile("[A-Z]")
        regex_numero = re.compile("[0-9]")
        if re.search(regex_simbolos, self.senha.data) == None or re.search(regex_minuscula, self.senha.data) == None \
                or re.search(regex_maiuscula, self.senha.data) == None or re.search(regex_numero, self.senha.data) == None \
                or len(self.senha.data) < 10:
            self.erros["senha"] = "A senha deve ter pelo menos um caractere especial, uma letra maiúscula e minúscula, um número e 10 caracteres ao menos"

        if len(self.erros.items()) > 0:
            return False
        return True
    
class FormularioRemocao(FlaskForm):

    class Meta:
        csrf = True

    usuario = StringField('', [InputRequired("Insira o usuário para cadastro")], render_kw=dict(placeholder=""))

    def validate(self, extra_validators):
        validacao_form = super(FormularioRemocao, self).validate()
        if not validacao_form:
            if self.usuario.data == "":
                self.erros["usuario"] = "Digite um nome de usuário"
            return False
        if self.usuario.data == current_user.usuario:
            self.erros["usuario"] = "O usuário a ser deletado não pode ser igual ao atual"
            return False
        usuario = db.session.execute(db.select(Usuario).filter_by(usuario = self.usuario.data)).first()
        if usuario == None:
            self.erros["usuario"] = "Usuário não cadastrado"
            return False
        return True
