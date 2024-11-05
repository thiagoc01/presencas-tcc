from flask import Blueprint, redirect, render_template, request, url_for, abort
from flask_login import login_user, logout_user, current_user, login_required
from presencas import bcrypt_var, db, app
from .usuario import Usuario
from .login import FormularioLogin
from .controle_usuario import FormularioCadastro, FormularioRemocao, FormularioAlteracaoSenha
from sqlalchemy.exc import DBAPIError, OperationalError
from logging import SUCCESS

cadastro_blueprint = Blueprint("cadastro", __name__)

@cadastro_blueprint.route("/login/", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("menu"))

    form = FormularioLogin(request.form)
    form.erros = dict()

    if form.validate_on_submit():

        try:

            usuario = db.session.execute(db.select(Usuario).filter_by(usuario = form.usuario.data)).first()

        except (DBAPIError, OperationalError) as e:

            abort(500, description = e)
        
        if usuario and bcrypt_var.check_password_hash(usuario[0].senha, form.senha.data):

            login_user(usuario[0], remember = form.lembrar_me.data)
            app.logger.log(SUCCESS, f"{current_user.usuario} | Usuário logado")
            return redirect(url_for("menu"))

        else:

            form.erros['login'] = 'Nome de usuário ou senha incorretos'

    return render_template("login/login.html", form = form)

@cadastro_blueprint.route("/logout/")
@login_required
def logout():

    if current_user.is_authenticated:
        app.logger.log(SUCCESS, f"{current_user.usuario} | Usuário saiu")
        logout_user()

    return redirect(url_for("cadastro.login"))

@cadastro_blueprint.route("/criar_usuario/", methods=['GET', 'POST'])
@login_required
def criar_usuario():

    if not current_user.e_adm and not current_user.e_superadm:

        abort(403)

    form = FormularioCadastro(request.form)
    form.erros = dict()

    if form.validate_on_submit():

        erro = None

        try:

            usuario = Usuario(usuario = form.usuario.data, senha = form.senha.data, e_adm = form.e_adm.data)

            db.session.add(usuario)
            db.session.commit()
            app.logger.log(SUCCESS, f"{current_user.usuario} | Usuário {form.usuario.data} {"(administrador)" if form.e_adm else ""} criado")

        except (DBAPIError, OperationalError) as e:
            app.logger.error(f"{current_user.usuario} | Erro ao criar usuário {form.usuario.data} {"(administrador)" if form.e_adm else ""}")
            erro = e

        except Exception as e:
            app.logger.error(f"{current_user.usuario} | Erro ao criar usuário {form.usuario.data} {"(administrador)" if form.e_adm else ""}")
            abort(500, description = e)

        return render_template('cadastro/log_cadastro.html', usuario = form.usuario.data, erro = erro, cadastrar_usuario = True)

    return render_template('cadastro/cadastro_usuario.html', form = form, cadastrar_usuario = True)

@cadastro_blueprint.route("/remover_usuario/", methods=['GET', 'POST'])
@login_required
def remover_usuario():

    if not current_user.e_adm and not current_user.e_superadm:

        abort(403)

    form = FormularioRemocao(request.form)
    form.erros = dict()

    if form.validate_on_submit():

        erro = None

        try:

            usuario = db.session.execute(db.select(Usuario).filter_by(usuario = form.usuario.data)).first()[0]
            db.session.delete(usuario)
            db.session.commit()
            app.logger.log(SUCCESS, f"{current_user.usuario} | Usuário {form.usuario.data} {"(administrador)" if usuario.e_adm else ""} removido")

        except (DBAPIError, OperationalError) as e:

            app.logger.error(f"{current_user.usuario} | Erro ao remover usuário {form.usuario.data}")
            erro = e

        except Exception as e:

            app.logger.error(f"{current_user.usuario} | Erro ao remover usuário {form.usuario.data}")
            abort(500, description = e)

        return render_template('cadastro/log_cadastro.html', usuario = form.usuario.data, erro = erro, cadastrar_usuario = False)

    return render_template('cadastro/cadastro_usuario.html', form = form, cadastrar_usuario = False)

@cadastro_blueprint.route("/alterar_senha/", methods=['GET', 'POST'])
@login_required
def alterar_senha():

    form = FormularioAlteracaoSenha(request.form)
    form.erros = dict()

    if form.validate_on_submit():

        erro = None

        try:

            usuario = db.session.execute(db.select(Usuario).filter_by(usuario = current_user.usuario)).first()[0]
            usuario.senha = bcrypt_var.generate_password_hash(form.senha.data)
            db.session.commit()
            app.logger.log(SUCCESS, f"{current_user.usuario} | Senha alterada com sucesso")

        except (DBAPIError, OperationalError) as e:

            app.logger.error(f"{current_user.usuario} | Erro ao alterar senha")
            erro = e

        except Exception as e:

            app.logger.error(f"{current_user.usuario} | Erro ao alterar senha")
            abort(500, description = e)

        return render_template('cadastro/log_alteracao_senha.html', erro = erro)

    return render_template('cadastro/alteracao_senha.html', form = form)