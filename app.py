from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from forms import FormDeRegistro, FormDeLogin


# Configurar aplicação
app = Flask(__name__)
app.config["SECRET_KEY"] = "chave_secreta"


# Configurar a sessão de login
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configurar banco de dados
db = SQL("sqlite:///innovation-hub.db")


# Página inicial
@app.route("/")
def index():
    formDeRegistro = FormDeRegistro()

    return render_template("index.html", formDeRegistro=formDeRegistro, formDeLogin=FormDeLogin(), abrirModalDeRegistro=False, abrirModalDeLogin=False)


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

    # Redirect user to home page
    return redirect("/")


@app.route("/sair")
def logout():
    # Deslogar qualquer usuário que tenha logado anteriormente
    session.clear()

    return redirect("/")