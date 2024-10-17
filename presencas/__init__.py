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