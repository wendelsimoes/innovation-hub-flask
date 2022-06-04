from application import db, ma
from application.models.user import User, UserSchema
from application.models.categoria import Categoria, CategoriaSchema


Like_da_Proposta = db.Table('Like_da_Proposta',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('proposta_id', db.Integer, db.ForeignKey('propostas.id'))
)


UserProposta = db.Table('UserProposta',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('proposta_id', db.Integer, db.ForeignKey('propostas.id'))
)


Proposta_Favorita = db.Table('Proposta_Favorita',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('proposta_id', db.Integer, db.ForeignKey('propostas.id'))
)


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
    privado = db.Column("privado", db.Boolean())
    likes = db.relationship("User", secondary=Like_da_Proposta, backref="likesPropostas")
    tipo_proposta = db.Column(db.String(200), nullable=False)
    gerente_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    gerente_de_projeto = db.relationship("User", backref="propostas_que_sou_gerente")
    membros = db.relationship("User", secondary=UserProposta, backref="propostas_que_estou")
    favoritadores = db.relationship("User", secondary=Proposta_Favorita, backref="propostas_favoritas")
    contador_de_like = db.Column(db.Integer)
    categorias = db.relationship("Categoria", backref="proposta")


class PropostaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Proposta
    
    likes = ma.Nested(UserSchema, many=True)
    favoritadores = ma.Nested(UserSchema, many=True)
    categorias = ma.Nested(CategoriaSchema, many=True)