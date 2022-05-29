from flask import flash, redirect, render_template, request
from flask_login import login_required, login_user, logout_user, login_manager, current_user
from application import app, login_manager, db
from application.forms import FormDeLogin, FormDeRegistro, FormDeProposta
from application.models import User


# Popular campos de categorias da proposta
categorias = {
    "Arte e Cultura": 0,
    "Música e Entretenimento": 1,
    "Automoveis e Veiculos": 2,
    "Informatica e Eletrônica": 3,
    "Educação": 4,
    "Vida": 5,
    "Família": 6,
    "Negócios e Empreendedorismo": 7,
    "Culinária e Gastronomia": 8,
    "Saúde e Bem Estar": 9,
    "Esporte": 10,
    "Viagem e Turismo": 11,
    "Economia e Finanças": 12,
    "Política e Mundo": 13,
    "Ciência e Tecnologia": 14,
    "Trabalho e Carreira": 15,
    "Psicologia e Sociedade": 16,
    "Meio Ambiente": 17
}


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


# Página inicial
@app.route("/")
def index():
    formDeRegistro = FormDeRegistro()
    return render_template("index.html", formDeRegistro=formDeRegistro, formDeLogin=FormDeLogin(), abrirModalDeRegistro=False, abrirModalDeLogin=False, user=current_user)


# Feed
@app.route("/feed")
@login_required
def feed():
    formDeProposta = FormDeProposta()
    return render_template("feed.html", formDeProposta=formDeProposta, categorias=categorias, user=current_user)


# Registrar
@app.route("/registrar", methods=["POST"])
def registrar():
    formDeRegistro = FormDeRegistro()

    if not formDeRegistro.validate_on_submit():
        return render_template("index.html", formDeRegistro=formDeRegistro, formDeLogin=FormDeLogin(), abrirModalDeRegistro=True, abrirModalDeLogin=False)

    novo_usuario = User(formDeRegistro.email.data, formDeRegistro.nome.data, formDeRegistro.sobrenome.data, formDeRegistro.nascimento.data.day, formDeRegistro.nascimento.data.month, formDeRegistro.nascimento.data.year, formDeRegistro.apelido.data, formDeRegistro.senha.data)

    db.session.add(novo_usuario)

    db.session.commit()

    return redirect("/")


@app.route("/entrar", methods=["POST"])
def login():
    formDeLogin = FormDeLogin()

    if not formDeLogin.validate_on_submit():
        return render_template("index.html", formDeRegistro=FormDeRegistro(), formDeLogin=formDeLogin, abrirModalDeRegistro=False, abrirModalDeLogin=True)
    
    # Logar
    user = User.query.filter_by(apelido=formDeLogin.apelido.data).first()

    if request.form.get("lembrar_de_mim") == "on":
        login_user(user, remember=True)
    else:
        login_user(user)
        
    # Redirect user to home page
    return redirect("/")


@app.route("/sair")
def logout():
    # Deslogar qualquer usuário que tenha logado anteriormente
    logout_user()

    return redirect("/")


@login_manager.unauthorized_handler
def unauthorized():
    # Mostrar uma página de erro
    return render_template("erro.html", codigo=403, mensagem="NÃO AUTORIZADO - LOGIN NECESSÁRIO")