from application import db
from werkzeug.security import check_password_hash
from flask_login import UserMixin


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
    quem_pediu_para_entrar_foto = db.Column(db.String(1000), nullable=False)
    titulo_da_proposta = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    proposta_id = db.Column(db.Integer, db.ForeignKey("propostas.id"))
    dia_criacao = db.Column(db.Integer, nullable=False)
    mes_criacao = db.Column(db.Integer, nullable=False)
    ano_criacao = db.Column(db.Integer, nullable=False)
    