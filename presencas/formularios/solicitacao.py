from flask import session
from presencas import db

class Solicitacao(db.Model):

    __tablename__ = "solicitacoes"

    sessao = db.Column(db.String, primary_key=True)
    id = db.Column(db.String, primary_key=True)
    progresso = db.Column(db.Double)

    def __init__(self, id):
        self.sessao = session.get('_id')
        self.id = id
        self.progresso = 0

    def __repr__(self):
        return f"<Solicitação {self.sessao} {self.id}>"