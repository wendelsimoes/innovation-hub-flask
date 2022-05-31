from application import db
from werkzeug.security import check_password_hash
from flask_login import UserMixin


UserProposta = db.Table('UserProposta',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('proposta_id', db.Integer, db.ForeignKey('propostas.id'))
)

Like_da_Proposta = db.Table('Like_da_Proposta',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('proposta_id', db.Integer, db.ForeignKey('propostas.id'))
)

Like_do_Comentario = db.Table('Like_do_Comentario',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('comentario_id', db.Integer, db.ForeignKey('comentarios.id'))
)

Proposta_Favorita = db.Table('Proposta_Favorita',
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
    propostas_que_estou = db.relationship("Proposta", secondary=UserProposta, backref="membro")
    propostas_que_sou_gerente = db.relationship("Proposta", backref="gerente_de_projeto")
    meus_comentarios = db.relationship("Comentario", backref="user")
    propostas_que_dei_like = db.relationship("Proposta", secondary=Like_da_Proposta, backref="likes")
    comentarios_que_dei_like = db.relationship("Comentario", secondary=Like_do_Comentario, backref="likes")
    propostas_favoritas = db.relationship("Proposta", secondary=Proposta_Favorita, backref="favoritador")
    notificacoes_pedir_para_participar = db.relationship("Notificacoes_Pedir_para_Participar", backref="gerente_da_proposta")

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
    tipo_proposta = db.Column(db.String(200), nullable=False)
    gerente_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    categorias = db.relationship("Categoria", backref="proposta")
    comentarios = db.relationship("Comentario", backref="proposta")


class Categoria(db.Model):
    __tablename__ = "categorias"

    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column("nome", db.String(200), nullable=False)
    valor = db.Column("valor", db.Integer, nullable=False)
    proposta_id = db.Column(db.Integer, db.ForeignKey("propostas.id"))


class Comentario(db.Model):
    __tablename__ = "comentarios"

    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    texto_comentario = db.Column("texto_comentario", db.String(1000), nullable=False)
    dia_criacao = db.Column(db.Integer, nullable=False)
    mes_criacao = db.Column(db.Integer, nullable=False)
    ano_criacao = db.Column(db.Integer, nullable=False)
    dono_do_comentario = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    proposta_id = db.Column(db.Integer, db.ForeignKey("propostas.id"))


class Notificacoes_Pedir_para_Participar(db.Model):
    __tablename__ = "notificacoes_pedir_para_participar"

    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    quem_pediu_para_entrar = db.Column(db.String(200), nullable=False)
    titulo_da_proposta = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    proposta_id = db.Column(db.Integer, db.ForeignKey("propostas.id"))
    