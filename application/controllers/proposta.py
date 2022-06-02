from application import app, db
from flask_login import login_required, current_user
from application.models.proposta import Proposta
from flask import render_template, request, Response
from application.models.categorias import categorias
import json


@app.route("/arquivadas", methods=["GET"])
@login_required
def arquivadas():
    todas_propostas_arquivadas_e_nao_privadas = Proposta.query.filter_by(privado=False, arquivado=True).all()

    return render_template("arquivadas.html", categorias=categorias, user=current_user, todas_propostas_arquivadas_e_nao_privadas=todas_propostas_arquivadas_e_nao_privadas)


@app.route("/likear_proposta", methods=["POST"])
@login_required
def likear_proposta():
    proposta_a_likear = Proposta.query.filter_by(id=request.form.get("id_proposta")).first()

    if proposta_a_likear:
        propostas_que_dei_like = current_user.propostas_que_dei_like

        if proposta_a_likear in propostas_que_dei_like:
            current_user.propostas_que_dei_like.remove(proposta_a_likear)
            db.session.commit()
            return Response(json.dumps({ "likeado": False, "numeros_de_like": len(proposta_a_likear.likes) }))
        else:
            current_user.propostas_que_dei_like.append(proposta_a_likear)
            db.session.commit()
            return Response(json.dumps({ "likeado": True, "numeros_de_like": len(proposta_a_likear.likes) }))
    else:
        return render_template("erro.html", codigo=404, mensagem="ERRO NO SERVER - PROPOSTA NÃO ENCONTRADA")