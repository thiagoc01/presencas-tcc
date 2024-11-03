from flask_login import UserMixin
from presencas import bcrypt_var, db
from sqlalchemy import false

class Usuario(db.Model, UserMixin):

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String, unique=True, nullable=False)
    senha = db.Column(db.String, nullable=False)
    e_adm = db.Column(db.Boolean, nullable=False, server_default = false())
    e_superadm = db.Column(db.Boolean, nullable=False, server_default = false())

    def __init__(self, usuario, senha, e_adm=False, e_superadm=False):
        self.usuario = usuario
        self.senha = bcrypt_var.generate_password_hash(senha)
        self.e_adm = e_adm
        self.e_superadm = e_superadm

    def __repr__(self):
        return f"<Usuário {self.usuario}>"