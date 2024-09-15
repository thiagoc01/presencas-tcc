from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login.login'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from presencas.login.views import login_blueprint
from presencas.formularios.views import formulario_blueprint

app.register_blueprint(login_blueprint)
app.register_blueprint(formulario_blueprint)

from presencas.login.models import Usuario

@login_manager.user_loader
def load_user(id_usuario):
    return Usuario.query.filter(Usuario.id == int(id_usuario)).first()
