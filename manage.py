from flask.cli import FlaskGroup

from presencas import app, db
from presencas.cadastro.usuario import Usuario
import re

def _verifica_minimalidade_senha(senha):

    regex_simbolos = re.compile("[@_!#$%^&*()<>?/\|}{~:\.]")
    regex_minuscula = re.compile("[a-z]")
    regex_maiuscula = re.compile("[A-Z]")

    regex_numero = re.compile("[0-9]")

    if re.search(regex_simbolos, senha) == None or re.search(regex_minuscula, senha) == None \
            or re.search(regex_maiuscula, senha) == None or re.search(regex_numero, senha) == None \
            or len(senha) < 10:

        return 1

cli = FlaskGroup(app)

import getpass

@cli.command("criar_super_administrador")
def criar_superadm():

    usuario = input("Insira o nome de usuário: ")
    senha = getpass.getpass("Insira a senha: ")
    confirmar_senha = getpass.getpass("Confirme a senha: ")

    if senha != confirmar_senha:
        print("As senhas digitadas não são iguais")
        return

    if _verifica_minimalidade_senha(senha) == 1:
        print("A senha deve ter pelo menos um caractere especial, uma letra maiúscula e minúscula, um número e 10 caracteres ao menos")
        return 1

    try:

        usuario = Usuario(usuario=usuario, senha=senha, e_adm=True, e_superadm=True)
        db.session.add(usuario)
        db.session.commit()
        print("Usuário criado com sucesso")

    except Exception:

        print("Não foi possível criar o superusuário")

@cli.command("remover_super_administrador")
def remover_superadm():

    nome_usuario = input("Insira o nome de usuário: ")

    try:

        usuario = db.session.execute(db.select(Usuario).filter_by(usuario = nome_usuario)).first()[0]
        db.session.delete(usuario)
        db.session.commit()
        print("Usuário removido com sucesso")

    except Exception:

        print("Não foi possível remover o superusuário")


if __name__ == "__main__":
    cli()