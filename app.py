from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from datetime import date


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


# Form de registro
class FormDeRegistro(FlaskForm):
    email = EmailField("Email", validators=[
        InputRequired("Este campo é necessário")])

    nome = StringField("Nome", validators=[
        InputRequired("Este campo é necessário"), 
        Length(min=3, max=200, message="Campo deve conter entre 3 e 200 caracteres")])

    sobrenome = StringField("Sobrenome", validators=[
        InputRequired("Este campo é necessário"), 
        Length(min=3, max=200, message="Campo deve conter entre 3 e 200 caracteres")])

    nascimento = DateField("Nascimento", validators=[
        InputRequired("Este campo é necessário")])

    apelido = StringField("Apelido", validators=[
        InputRequired("Este campo é necessário"), 
        Length(min=3, max=200, message="Campo deve conter entre 3 e 200 caracteres")])

    senha = PasswordField("Senha", validators=[
        InputRequired("Este campo é necessário"), 
        Length(min=3, max=200, message="Campo deve conter entre 3 e 200 caracteres"), 
        EqualTo("confirmar_senha", message="As senhas devem ser iguais")])

    confirmar_senha = PasswordField("Confirmar Senha", validators=[
        InputRequired("Este campo é necessário"), 
        Length(min=3, max=200, message="Campo deve conter entre 3 e 200 caracteres")])


    def validate_apelido(self, apelido):
        apelidoSeExistir = db.execute(
            "SELECT apelido FROM users WHERE apelido = ?", apelido.data)

        if len(apelidoSeExistir) > 0:
            raise ValidationError("Este apelido já está em uso")


    def validate_nascimento(self, nascimento):
        if nascimento.data > date.today():
            raise ValidationError("Data de nascimento deve ser maior que data atual")