from application import app, db
from flask_login import login_required, current_user
from application.models.comentario import Comentario, ComentarioSchema
from application.models.proposta import Proposta
from flask import request, Response, render_template, redirect, url_for
import json
from datetime import date
from flask import jsonify


@app.route("/comentar", methods=["POST"])
@login_required
def comentar():
    proposta_a_comentar = Proposta.query.filter_by(id=request.form.get("id_proposta")).first()

    if proposta_a_comentar:
        if not request.form.get("texto_comentario"):
            return Response(json.dumps({"status": 400, "mensagem": "Este campo é necessário"}), mimetype="application\json")

        if len(request.form.get("texto_comentario")) > 1000:
            return Response(json.dumps({"status": 400, "mensagem": "Campo deve conter no máximo 1000 caracteres"}), mimetype="application\json")

        today = date.today()
        novo_comentario = Comentario(texto_comentario=request.form.get("texto_comentario"), dia_criacao=today.day, mes_criacao=today.month, ano_criacao=today.year, dono_do_comentario=current_user.apelido, proposta_id=proposta_a_comentar.id, user=current_user, proposta=proposta_a_comentar)

        db.session.commit()

        return redirect(url_for("carregar_comentarios", id_proposta=request.form.get("id_proposta")))
    else:
        return render_template("erro.html", codigo=404, mensagem="ERRO NO SERVER - PROPOSTA NÃO ENCONTRADA")


@app.route("/likear_comentario", methods=["POST"])
@login_required
def likear_comentario():
    comentario_a_likear = Comentario.query.filter_by(id=request.form.get("id_comentario")).first()

    if comentario_a_likear:
        comentarios_que_dei_like = current_user.likes

        if comentario_a_likear in comentarios_que_dei_like:
            comentario_a_likear.likes.remove(current_user)
            db.session.commit()
            return Response(json.dumps({ "likeado": False, "numeros_de_like": len(comentario_a_likear.likes) }))
        else:
            comentario_a_likear.likes.append(current_user)
            db.session.commit()
            return Response(json.dumps({ "likeado": True, "numeros_de_like": len(comentario_a_likear.likes) }))
    else:
        return render_template("erro.html", codigo=404, mensagem="ERRO NO SERVER - COMENTARIO NÃO ENCONTRADO")


@app.route("/carregar_comentarios", methods=["GET"])
def carregar_comentarios():
    id_proposta = request.args.get("id_proposta")

    if id_proposta:
        comentarios_da_proposta = Comentario.query.filter_by(proposta_id=id_proposta).all()
        comentarios_que_dei_like = current_user.likes
        
        if len(comentarios_da_proposta) > 0:
            comentario_schema = ComentarioSchema(many=True)
            comentarios_da_proposta_formatado = comentario_schema.dump(comentarios_da_proposta)

            for comentario in comentarios_da_proposta_formatado:
                for user in comentario['likes']:
                    if current_user.apelido == user['apelido']:
                        comentario['likeado'] = True

            return jsonify(comentarios_da_proposta_formatado)
        else:
            return Response(json.dumps({"status": 200, "info": "Niguém fez um comentário ainda, que tal ser o primeiro?"}), mimetype="application\json")
    else:
        return render_template("erro.html", codigo=404, mensagem="ERRO NO SERVER - PROPOSTA NÃO ENCONTRADA")