from application import db, ma
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from application.models.notificacoes_pedir_para_participar import Notificacoes_Pedir_para_Participar
from application.models.proposta import Proposta
from application.models.categoria import Categoria


UserProposta = db.Table('UserProposta',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('proposta_id', db.Integer, db.ForeignKey('propostas.id'))
)

Like_da_Proposta = db.Table('Like_da_Proposta',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('proposta_id', db.Integer, db.ForeignKey('propostas.id'))
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
    propostas_que_dei_like = db.relationship("Proposta", secondary=Like_da_Proposta, backref="likes")
    propostas_favoritas = db.relationship("Proposta", secondary=Proposta_Favorita, backref="favoritador")
    notificacoes_pedir_para_participar = db.relationship("Notificacoes_Pedir_para_Participar", backref="gerente_da_proposta")
    foto_perfil = db.Column(db.String(1000))

    def verificar_senha_encriptada(self, senha):
        return check_password_hash(self.senha_encriptada, senha)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User