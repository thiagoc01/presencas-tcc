from flask_login import UserMixin
from presencas import bcrypt_var, db

class Usuario(db.Model, UserMixin):

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String, unique=True, nullable=False)
    senha = db.Column(db.String, nullable=False)
    e_adm = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, usuario, senha, e_adm=False):
        self.usuario = usuario
        self.senha = bcrypt_var.generate_password_hash(senha)
        self.e_adm = e_adm

    def __repr__(self):
        return f"<Usuário {self.usuario}>"
    

