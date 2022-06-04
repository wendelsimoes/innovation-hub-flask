from application import db, ma


class Categoria(db.Model):
    __tablename__ = "categorias"

    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column("nome", db.String(200), nullable=False)
    valor = db.Column("valor", db.Integer, nullable=False)
    proposta_id = db.Column(db.Integer, db.ForeignKey("propostas.id"))


class CategoriaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Categoria