from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

# Configurar aplicação
app = Flask(__name__)

# Configurar a sessão de login
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configurar banco de dados
db = SQL("sqlite:///innovation-hub.db")

# Página inicial
@app.route("/")
def index():
    return render_template("index.html")