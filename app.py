from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from forms import FormDeRegistro, FormDeLogin, FormDeProposta
from flask_login import LoginManager, login_required, login_user, UserMixin, logout_user
from helpers import User
from ast import literal_eval
from categorias import categorias


# Configurar aplicação
app = Flask(__name__)
app.config["SECRET_KEY"] = "chave_secreta"


# Configurar a sessão de login
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configurar login geral para bloquar acesso de alguma páginas
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User(literal_eval(user_id)["id"])


@login_manager.unauthorized_handler
def unauthorized():
    # Mostrar uma página de erro
    return render_template("erro.html", codigo=403, mensagem="NÃO AUTORIZADO - LOGIN NECESSÁRIO")

# Configurar banco de dados
db = SQL("sqlite:///innovation-hub.db")


# Página inicial
@app.route("/")
def index():
    formDeRegistro = FormDeRegistro()

    return render_template("index.html", formDeRegistro=formDeRegistro, formDeLogin=FormDeLogin(), abrirModalDeRegistro=False, abrirModalDeLogin=False)


# Feed
@app.route("/feed")
@login_required
def feed():
    formDeProposta = FormDeProposta()
    return render_template("feed.html", formDeProposta=formDeProposta, categorias=categorias)


# Registrar
@app.route("/registrar", methods=["POST"])
def registrar():
    formDeRegistro = FormDeRegistro()

    if not formDeRegistro.validate_on_submit():
        return render_template("index.html", formDeRegistro=formDeRegistro, formDeLogin=FormDeLogin(), abrirModalDeRegistro=True, abrirModalDeLogin=False)

    db.execute("INSERT INTO users (email, nome, sobrenome, dia_nascimento, mes_nascimento, ano_nascimento, apelido, senha) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", formDeRegistro.email.data, formDeRegistro.nome.data,
               formDeRegistro.sobrenome.data, formDeRegistro.nascimento.data.day, formDeRegistro.nascimento.data.month, formDeRegistro.nascimento.data.year, formDeRegistro.apelido.data, formDeRegistro.senha.data)

    return redirect("/")


@app.route("/entrar", methods=["POST"])
def login():
    formDeLogin = FormDeLogin()

    if not formDeLogin.validate_on_submit():
        return render_template("index.html", formDeRegistro=FormDeRegistro(), formDeLogin=formDeLogin, abrirModalDeRegistro=False, abrirModalDeLogin=True)
    
    # Deslogar qualquer usuário que tenha logado anteriormente
    session.clear()

    # Logar
    user = db.execute("SELECT * FROM users WHERE apelido = ?", formDeLogin.apelido.data)[0]
    
    session["user_id"] = user["id"]
    session["nome"] = user["nome"]
    session["apelido"] = user["apelido"]

    userLogin = User(user["id"])
    login_user(userLogin)

    # Redirect user to home page
    return redirect("/")

@app.route("/sair")
def logout():
    # Deslogar qualquer usuário que tenha logado anteriormente
    session.clear()
    logout_user()

    return redirect("/")