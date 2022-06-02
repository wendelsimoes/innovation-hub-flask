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


@app.route("/favoritar", methods=["POST"])
@login_required
def favoritar():
    proposta_a_favoritar = Proposta.query.filter_by(id=request.form.get("id_proposta")).first()

    if proposta_a_favoritar:
        propostas_favoritas = current_user.propostas_favoritas
        propostas_que_participo = current_user.propostas_que_estou

        if proposta_a_favoritar in propostas_que_participo:
            return Response(json.dumps({"status": 400, "mensagem": "Você não pode favoritar uma proposta que participe"}))

        if proposta_a_favoritar in propostas_favoritas:
            current_user.propostas_favoritas.remove(proposta_a_favoritar)
            db.session.commit()
            return Response(json.dumps({"favoritado": False, "mensagem": "Proposta removida dos favoritos", "status": 200}))
        else:
            current_user.propostas_favoritas.append(proposta_a_favoritar)
            db.session.commit()
            return Response(json.dumps({"favoritado": True, "mensagem": "Proposta adicionada aos favoritos", "status": 200}))
    else:
        return render_template("erro.html", codigo=404, mensagem="ERRO NO SERVER - PROPOSTA NÃO ENCONTRADA")