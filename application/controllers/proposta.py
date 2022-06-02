from application import app
from flask_login import login_required, current_user
from application.models.proposta import Proposta
from flask import render_template
from application.models.categorias import categorias


@app.route("/arquivadas", methods=["GET"])
@login_required
def arquivadas():
    todas_propostas_arquivadas_e_nao_privadas = Proposta.query.filter_by(privado=False, arquivado=True).all()

    return render_template("arquivadas.html", categorias=categorias, user=current_user, todas_propostas_arquivadas_e_nao_privadas=todas_propostas_arquivadas_e_nao_privadas)