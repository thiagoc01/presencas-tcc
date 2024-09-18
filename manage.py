from flask.cli import FlaskGroup

from presencas import app, db
from presencas.cadastro.usuario import Usuario

cli = FlaskGroup(app)

import getpass


@cli.command("create_admin")
def create_admin():
    """Creates the admin user."""
    usuario = input("Enter email address: ")
    password = getpass.getpass("Enter password: ")
    confirm_password = getpass.getpass("Enter password again: ")
    if password != confirm_password:
        print("Passwords don't match")
        return 1
    try:
        usuario = Usuario(usuario=usuario, senha=password, e_adm=True)
        db.session.add(usuario)
        db.session.commit()
    except Exception:
        print("Couldn't create admin user.")


if __name__ == "__main__":
    cli()