from flask import render_template
from flask_login import login_manager
from application import login_manager, db, app
from application.models.user import User
from application.semeador_de_dados import semear_banco


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@login_manager.unauthorized_handler
def unauthorized():
    # Mostrar uma página de erro
    return render_template("erro.html", codigo=403, mensagem="NÃO AUTORIZADO - LOGIN NECESSÁRIO")


from application.controllers import home
from application.controllers import user
from application.controllers import feed
from application.controllers import proposta
from application.controllers import comentario

db.create_all()
#semear_banco()
app.run(debug=True)