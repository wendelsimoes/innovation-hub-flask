from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from datetime import date
from cs50 import SQL

# Configurar banco de dados
db = SQL("sqlite:///innovation-hub.db")

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
            raise ValidationError("Data de nascimento deve ser menor que data atual")


# Form de login
class FormDeLogin(FlaskForm):
    apelido = StringField("Apelido", validators=[
        InputRequired("Este campo é necessário"), 
        Length(min=3, max=200, message="Campo deve conter entre 3 e 200 caracteres")])

    senha = PasswordField("Senha", validators=[
        InputRequired("Este campo é necessário"), 
        Length(min=3, max=200, message="Campo deve conter entre 3 e 200 caracteres")])

    def validate_apelido(self, apelido):
        apelidoSeExistir = db.execute(
            "SELECT apelido FROM users WHERE apelido = ?", apelido.data)

        if len(apelidoSeExistir) == 0:
            raise ValidationError("Apelido não encontrado")

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        
        match = db.execute("SELECT apelido FROM users WHERE apelido = ? AND senha = ?", self.apelido.data, self.senha.data)

        if len(match) == 0:
            self.senha.errors.append("Senha invalida")
            return False
        return True