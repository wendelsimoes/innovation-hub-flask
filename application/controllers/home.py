from application import app
from application.forms import FormDeRegistro, FormDeLogin
from flask_login import current_user
from flask import render_template

# Página inicial
@app.route("/")
def index():
    formDeRegistro = FormDeRegistro()
    formDeLogin = FormDeLogin()
    return render_template("index.html", formDeRegistro=formDeRegistro, formDeLogin=formDeLogin, abrirModalDeRegistro=False, abrirModalDeLogin=False, user=current_user)