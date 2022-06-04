from application import app, db
from flask_login import login_required, current_user
from application.models.comentario import Comentario, ComentarioSchema
from application.models.proposta import Proposta
from flask import request, Response, render_template, redirect, url_for, jsonify
import json
from datetime import date
from flask import jsonify
from application.models.user import User, UserSchema
from sqlalchemy.sql.expression import desc


@app.route("/criar_comentario", methods=["POST"])
@login_required
def criar_comentario():
    proposta_a_comentar = Proposta.query.filter_by(id=request.form.get("id_proposta")).first()

    if proposta_a_comentar:
        if not request.form.get("texto_comentario"):
            return jsonify({"status": 400, "mensagem": "Este campo é necessário"})

        if len(request.form.get("texto_comentario")) > 1000:
            return jsonify({"status": 400, "mensagem": "Campo deve conter no máximo 1000 caracteres"})

        today = date.today()
        novo_comentario = Comentario(texto_comentario=request.form.get("texto_comentario"), dia_criacao=today.day, mes_criacao=today.month, ano_criacao=today.year, dono_do_comentario=current_user.apelido, proposta_id=proposta_a_comentar.id, user=current_user, proposta=proposta_a_comentar, contador_de_like=0)

        proposta_a_comentar.comentarios.append(novo_comentario)
        db.session.commit()

        return redirect(url_for("carregar_comentarios", id_proposta=request.form.get("id_proposta")))
    else:
        return render_template("erro.html", codigo=404, mensagem="ERRO NO SERVER - PROPOSTA NÃO ENCONTRADA")


@app.route("/likear_comentario", methods=["POST"])
@login_required
def likear_comentario():
    comentario_a_likear = Comentario.query.filter_by(id=request.form.get("id_comentario")).first()
    comentario_a_likear_contador = comentario_a_likear.contador_de_like

    if comentario_a_likear:
        comentarios_que_dei_like = current_user.likesComentarios
        comentario_schema = ComentarioSchema()
        user_schema = UserSchema()

        if comentario_a_likear in comentarios_que_dei_like:
            comentario_a_likear.likes.remove(current_user)
            comentario_a_likear.contador_de_like = comentario_a_likear_contador - 1
            db.session.commit()
        else:
            comentario_a_likear.likes.append(current_user)
            comentario_a_likear.contador_de_like = comentario_a_likear_contador + 1
            db.session.commit()

        return jsonify({ "comentario": comentario_schema.dump(comentario_a_likear), "user": user_schema.dump(current_user) })
    else:
        return render_template("erro.html", codigo=404, mensagem="ERRO NO SERVER - COMENTARIO NÃO ENCONTRADO")


@app.route("/carregar_comentarios", methods=["GET"])
def carregar_comentarios():
    id_proposta = request.args.get("id_proposta")
    ordenar = request.args.get("ordenar")

    if id_proposta:
        comentarios_da_proposta = Comentario.query.filter_by(proposta_id=id_proposta)
        
        if len(comentarios_da_proposta.all()) > 0:
            comentario_schema = ComentarioSchema(many=True)
            user_schema = UserSchema()

            if ordenar == "popular":
                return jsonify({ "comentarios": comentario_schema.dump(comentarios_da_proposta.order_by(desc(Comentario.contador_de_like)).all()), "user": user_schema.dump(current_user) })
            else:
                return jsonify({ "comentarios": comentario_schema.dump(comentarios_da_proposta.order_by(desc(Comentario.ano_criacao)).order_by(desc(Comentario.mes_criacao)).order_by(desc(Comentario.dia_criacao)).all()), "user": user_schema.dump(current_user) })
        else:
            return jsonify({ "status": 100, "info": "Niguém fez um comentário ainda, que tal ser o primeiro?" })
    else:
        return render_template("erro.html", codigo=404, mensagem="ERRO NO SERVER - PROPOSTA NÃO ENCONTRADA")