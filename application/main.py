from flask import flash, redirect, render_template, request, Response, url_for
from flask_login import login_required, login_user, logout_user, login_manager, current_user
from application import app, login_manager, db
from application.forms import FormDeLogin, FormDeRegistro, FormDeProposta, FormDeConfiguracao

from application.models.user import User
from application.models.proposta import Proposta


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


from application.controllers import home
from application.controllers import user
from application.controllers import feed
from application.controllers import proposta
from application.controllers import comentario


@app.route("/entrar", methods=["POST"])
def login():
    formDeLogin = FormDeLogin()

    if not formDeLogin.validate_on_submit():
        return render_template("index.html", formDeRegistro=FormDeRegistro(), formDeLogin=formDeLogin, abrirModalDeRegistro=False, abrirModalDeLogin=True, user=current_user)
    
    # Logar
    user = User.query.filter_by(apelido=formDeLogin.apelido.data).first()

    if request.form.get("lembrar_de_mim") == "on":
        login_user(user, remember=True)
    else:
        login_user(user)
        
    # Redirect user to home page
    return redirect(url_for("index"))


@app.route("/sair")
def logout():
    # Deslogar qualquer usuário que tenha logado anteriormente
    logout_user()

    return redirect(url_for("index"))


@login_manager.unauthorized_handler
def unauthorized():
    # Mostrar uma página de erro
    return render_template("erro.html", codigo=403, mensagem="NÃO AUTORIZADO - LOGIN NECESSÁRIO")


db.create_all()