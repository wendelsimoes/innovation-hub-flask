from application import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(200), nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    sobrenome = db.Column(db.String(200), nullable=False)
    dia_nascimento = db.Column(db.Integer, nullable=False)
    mes_nascimento = db.Column(db.Integer, nullable=False)
    ano_nascimento = db.Column(db.Integer, nullable=False)
    apelido = db.Column(db.String(200), nullable=False, unique=True)
    senha_encriptada = db.Column(db.String(), nullable=False)

    def __init__(self, email, nome, sobrenome, dia_nascimento, mes_nascimento, ano_nascimento, apelido, senha):
        self.email = email
        self.nome = nome
        self.sobrenome = sobrenome
        self.dia_nascimento = dia_nascimento
        self.mes_nascimento = mes_nascimento
        self.ano_nascimento = ano_nascimento
        self.apelido = apelido
        self.senha_encriptada = generate_password_hash(senha)

    def verificar_senha_encriptada(self, senha):
        return check_password_hash(self.senha_encriptada, senha)