from application import app
from flask_login import login_required, current_user
from application.forms import FormDeProposta
from flask import render_template
from application.models.categorias import categorias
from application.models.tipo_proposta import tipo_proposta


@app.route("/feed", methods=["GET"])
@login_required
def feed():
    formDeProposta = FormDeProposta()

    return render_template("feed.html", formDeProposta=formDeProposta, categorias=categorias, tipo_proposta=tipo_proposta, user=current_user)