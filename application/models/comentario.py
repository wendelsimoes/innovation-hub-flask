from application import db


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