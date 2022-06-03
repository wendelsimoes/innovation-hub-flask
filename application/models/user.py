from application import db, ma
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from application.models.notificacoes_pedir_para_participar import Notificacoes_Pedir_para_Participar
from application.models.categoria import Categoria


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
    senha_encriptada = db.Column(db.String(200), nullable=False)
    notificacoes_pedir_para_participar = db.relationship("Notificacoes_Pedir_para_Participar", backref="gerente_da_proposta")
    foto_perfil = db.Column(db.String(1000))

    def verificar_senha_encriptada(self, senha):
        return check_password_hash(self.senha_encriptada, senha)


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    email = ma.auto_field()
    nome = ma.auto_field()
    sobrenome = ma.auto_field()
    dia_nascimento = ma.auto_field()
    mes_nascimento = ma.auto_field()
    ano_nascimento = ma.auto_field()
    apelido = ma.auto_field()
    notificacoes_pedir_para_participar =  ma.auto_field()
    foto_perfil = ma.auto_field()