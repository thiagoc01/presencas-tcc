from flask import Flask, redirect, url_for, render_template
from flask_login import LoginManager, login_required
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
bcrypt_var = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'cadastro.login'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from presencas.cadastro.views import cadastro_blueprint
from presencas.formularios.views import formulario_blueprint

app.register_blueprint(cadastro_blueprint)
app.register_blueprint(formulario_blueprint)

from presencas.cadastro.usuario import Usuario
from .formularios.solicitacao import Solicitacao

with app.app_context():
    solicitacoes_pendentes = db.session.execute(db.select(Solicitacao)).all()
    if solicitacoes_pendentes:
        for solicitacao in solicitacoes_pendentes:
            db.session.delete(solicitacao[0])
        db.session.commit()

@login_manager.user_loader
def load_user(id_usuario):
    return Usuario.query.filter(Usuario.id == int(id_usuario)).first()

@app.route("/", methods=["GET"])
def index():
    return redirect(url_for('cadastro.login'))

@app.route("/menu/", methods=["GET"])
@login_required
def menu():
    return render_template('menu.html')

@app.errorhandler(400)
def bad_request(e):
    return render_template('erros/400.html'), 400

@app.errorhandler(401)
def unauthorize(e):
    return render_template('erros/401.html'), 401

@app.errorhandler(403)
def forbidden(e):
    return render_template('erros/403.html'), 403

@app.errorhandler(404)
def not_found(e):
    return render_template('erros/404.html'), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('erros/405.html'), 405

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('erros/500.html'), 500

@app.errorhandler(502)
def bad_gateway(e):
    return render_template('erros/502.html'), 502

@app.errorhandler(504)
def gateway_timeout(e):
    return render_template('erros/504.html'), 504