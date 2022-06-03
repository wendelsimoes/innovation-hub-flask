from application import db, ma
from application.models.user import User, UserSchema
from application.models.proposta import Proposta


Like_do_Comentario = db.Table('Like_do_Comentario',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('comentario_id', db.Integer, db.ForeignKey('comentarios.id'))
)


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
    user = db.relationship("User", backref="comentarios")
    likes = db.relationship("User", secondary=Like_do_Comentario, backref="likes")
    proposta = db.relationship("Proposta", backref="comentarios")


class ComentarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comentario

    user = ma.Nested(UserSchema)