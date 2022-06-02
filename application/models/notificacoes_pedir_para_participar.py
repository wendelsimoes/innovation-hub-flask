from application import db


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