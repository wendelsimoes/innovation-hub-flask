from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from forms import FormDeRegistro


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

    return render_template("index.html", formDeRegistro=formDeRegistro)


# Registrar
@app.route("/registrar", methods=["POST"])
def registrar():
    formDeRegistro = FormDeRegistro()

    if not formDeRegistro.validate_on_submit():
        return render_template("index.html", formDeRegistro=formDeRegistro, openRegisterModal=True)

    db.execute("INSERT INTO users (email, nome, sobrenome, dia_nascimento, mes_nascimento, ano_nascimento, apelido, senha) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", formDeRegistro.email.data, formDeRegistro.nome.data,
               formDeRegistro.sobrenome.data, formDeRegistro.nascimento.data.day, formDeRegistro.nascimento.data.month, formDeRegistro.nascimento.data.year, formDeRegistro.apelido.data, formDeRegistro.senha.data)

    return redirect("/")