from flask_login import UserMixin
from presencas import bcrypt, db

class Usuario(UserMixin, db.Model):

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    senha = db.Column(db.String, nullable=False)
    e_adm = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, is_admin=False):
        self.email = email
        self.senha = bcrypt.generate_password_hash(password)
        self.e_adm = is_admin

    def __repr__(self):
        return f"<email {self.email}>"
    

