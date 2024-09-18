from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, current_user, login_required
from presencas import bcrypt_var, db
from .usuario import Usuario
from .login import FormularioLogin

login_blueprint = Blueprint("login", __name__)

@login_blueprint.route("/login/", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("formulario.index_formulario_criacao_artista"))

    form = FormularioLogin(request.form)

    if form.validate_on_submit():

        usuario = db.session.execute(db.select(Usuario).filter_by(usuario = form.usuario.data)).first()
        
        if usuario and bcrypt_var.check_password_hash(usuario[0].senha, form.senha.data):
            login_user(usuario[0], remember = form.lembrar_me.data)
            return redirect(url_for("formulario.index_formulario_criacao_artista"))

    return render_template("login/login.html", form = form)

@login_blueprint.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for("login.login"))