from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, EmailField, TextAreaField, IntegerField, BooleanField, validators
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from datetime import date
from application import db
from werkzeug.security import check_password_hash
from application.models import User
from flask_wtf.file import FileField, FileAllowed


# Form de Registro
class FormDeRegistro(FlaskForm):
    email = EmailField("Email", validators=[
        InputRequired("Este campo é necessário"), 
        Length(min=3, max=200, message="Campo deve conter entre 3 e 200 caracteres")])

    nome = StringField("Nome", validators=[
        InputRequired("Este campo é necessário"), 
        Length(min=3, max=200, message="Campo deve conter entre 3 e 200 caracteres")])

    sobrenome = StringField("Sobrenome", validators=[
        InputRequired("Este campo é necessário"), 
        Length(min=3, max=200, message="Campo deve conter entre 3 e 200 caracteres")])

    foto_perfil = FileField("Foto de Perfil", validators=[FileAllowed(['jpg', 'png'], message="Arquivo não suportado")])

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
        apelidoSeExistir = User.query.filter_by(apelido=apelido.data).first()

        if apelidoSeExistir:
            raise ValidationError("Este apelido já está em uso")


    def validate_nascimento(self, nascimento):
        if nascimento.data > date.today():
            raise ValidationError("Data de nascimento deve ser menor que data atual")


# Form de Login
class FormDeLogin(FlaskForm):
    apelido = StringField("Apelido", validators=[
        InputRequired("Este campo é necessário"), 
        Length(min=3, max=200, message="Campo deve conter entre 3 e 200 caracteres")])

    senha = PasswordField("Senha", validators=[
        InputRequired("Este campo é necessário"), 
        Length(min=3, max=200, message="Campo deve conter entre 3 e 200 caracteres")])

    def validate_apelido(self, apelido):
        apelidoSeExistir = User.query.filter_by(apelido=apelido.data).first()

        if not apelidoSeExistir:
            raise ValidationError("Apelido não encontrado")

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        
        valida_login = User.query.filter_by(apelido=self.apelido.data).first()

        if not check_password_hash(valida_login.senha_encriptada, self.senha.data):
            self.senha.errors.append("Senha invalida")
            return False
        return True


# Form de Proposta
class FormDeProposta(FlaskForm):
    titulo = StringField("Título", validators=[
        InputRequired("Este campo é necessário"), 
        Length(min=3, max=200, message="Campo deve conter entre 3 e 200 caracteres")], render_kw={"placeholder": "Título"})

    descricao = TextAreaField("Descrição", validators=[
        InputRequired("Este campo é necessário"), 
        Length(min=50, max=1000, message="Campo deve conter entre 50 e 1000 caracteres")], render_kw={"placeholder": "Descrição"})

    restricao_idade = IntegerField("Restrição de idade", validators=[validators.Optional()])

    membro = StringField("Membros", id="apelido_autocomplete", render_kw={"placeholder": "Pesquisar apelido"})

# Form de Configuração do usuário
class FormDeConfiguracao(FlaskForm):
    email = EmailField("Email", validators=[
        InputRequired("Este campo é necessário"), 
        Length(min=3, max=200, message="Campo deve conter entre 3 e 200 caracteres")])

    foto_perfil = FileField("Foto de Perfil", validators=[FileAllowed(['jpg', 'png'], message="Arquivo não suportado")])

    senha = PasswordField("Senha", validators=[
        InputRequired("Este campo é necessário"), 
        Length(min=3, max=200, message="Campo deve conter entre 3 e 200 caracteres"), 
        EqualTo("confirmar_senha", message="As senhas devem ser iguais")])

    confirmar_senha = PasswordField("Confirmar Senha", validators=[
        InputRequired("Este campo é necessário"), 
        Length(min=3, max=200, message="Campo deve conter entre 3 e 200 caracteres")])