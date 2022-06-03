from application import app, db
from flask_login import login_required, current_user
from application.models.proposta import Proposta
from flask import render_template, request, Response, url_for, redirect, jsonify
from application.models.categorias import categorias
import json
from datetime import date
from application.models.comentario import Comentario, ComentarioSchema


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
        novo_comentario = Comentario(texto_comentario=request.form.get("texto_comentario"), dia_criacao=today.day, mes_criacao=today.month, ano_criacao=today.year, dono_do_comentario=current_user.apelido, proposta=proposta_a_comentar)

        current_user.comentarios.append(novo_comentario)
        
        db.session.commit()

        return redirect(url_for("carregar_comentarios", id_proposta=request.form.get("id_proposta")))
    else:
        return render_template("erro.html", codigo=404, mensagem="ERRO NO SERVER - PROPOSTA NÃO ENCONTRADA")


@app.route("/carregar_comentarios", methods=["GET"])
def carregar_comentarios():
    id_proposta = request.args.get("id_proposta")

    if id_proposta:
        comentarios_da_proposta = Comentario.query.filter_by(proposta_id=id_proposta).all()
        comentarios_que_dei_like = current_user.likes
        
        if len(comentarios_da_proposta) > 0:
            comentario_schema = ComentarioSchema(many=True)
            comentarios_da_proposta_formatado = comentario_schema.dump(comentarios_da_proposta)

            todos_comentarios_da_proposta_array = []

            for comentario in comentarios_da_proposta:
                likeado = False
                if comentario in comentarios_que_dei_like:
                    likeado = True
                
                user = dict(comentario.user.__dict__)
                user.pop('_sa_instance_state', None)

                comentario_dicionario = dict(comentario.__dict__)
                comentario_dicionario.pop('_sa_instance_state', None)
                comentario_dicionario.pop('user', None)
                comentario_dicionario['user'] = user

                todos_comentarios_da_proposta_array.append(comentario_dicionario)

            return jsonify(comentarios_da_proposta_formatado)
        else:
            return Response(json.dumps({"status": 200, "info": "Niguém fez um comentário ainda, que tal ser o primeiro?"}), mimetype="application\json")
    else:
        return render_template("erro.html", codigo=404, mensagem="ERRO NO SERVER - PROPOSTA NÃO ENCONTRADA")