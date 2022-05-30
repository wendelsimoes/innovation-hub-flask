from application import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import date

UserProposta = db.Table('UserProposta',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('proposta_id', db.Integer, db.ForeignKey('propostas.id'))
)

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(200), nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    sobrenome = db.Column(db.String(200), nullable=False)
    dia_nascimento = db.Column(db.Integer, nullable=False)
    mes_nascimento = db.Column(db.Integer, nullable=False)
    ano_nascimento = db.Column(db.Integer, nullable=False)
    apelido = db.Column(db.String(200), nullable=False, unique=True)
    senha_encriptada = db.Column(db.String(), nullable=False)
    propostas_que_estou = db.relationship("Proposta", secondary=UserProposta, backref="membros")
    propostas_que_sou_gerente = db.relationship("Proposta", backref="gerente_de_projeto")

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


class Proposta(db.Model):
    __tablename__ = "propostas"

    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column("titulo", db.String(200), nullable=False)
    descricao = db.Column("descricao", db.String(1000), nullable=False)
    restricao_idade = db.Column("restricao_idade", db.Integer())
    arquivado = db.Column("arquivado", db.Boolean())
    dia_criacao = db.Column(db.Integer, nullable=False)
    mes_criacao = db.Column(db.Integer, nullable=False)
    ano_criacao = db.Column(db.Integer, nullable=False)
    votos = db.Column(db.Integer)
    privado = db.Column("privado", db.Boolean())
    gerente_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    categorias = db.relationship("Categoria", backref="proposta")

    def __init__(self, titulo, descricao, restricao_idade, privado):
        self.titulo = titulo
        self.descricao = descricao
        self.restricao_idade = restricao_idade
        self.privado = privado

        today = date.today()

        self.dia_criacao = today.day
        self.mes_criacao = today.month
        self.ano_criacao = today.year

        self.arquivado = False
        self.votos = 0


class Categoria(db.Model):
    __tablename__ = "categorias"

    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column("nome", db.String(200), nullable=False)
    valor = db.Column("valor", db.Integer, nullable=False)
    proposta_id = db.Column(db.Integer, db.ForeignKey("propostas.id"))