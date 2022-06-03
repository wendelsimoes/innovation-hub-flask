from application import app, db
from flask_login import login_required, current_user
from application.models.proposta import Proposta
from flask import render_template, request, Response, url_for, redirect, jsonify
from application.models.categorias import categorias
import json
from datetime import date
from application.models.comentario import Comentario, ComentarioSchema
from application.models.notificacoes_pedir_para_participar import Notificacoes_Pedir_para_Participar
from application.models.user import User
from application.forms import FormDeProposta


@app.route("/arquivadas", methods=["GET"])
@login_required
def arquivadas():
    todas_propostas_arquivadas_e_nao_privadas = Proposta.query.filter_by(privado=False, arquivado=True).all()

    return render_template("arquivadas.html", categorias=categorias, user=current_user, todas_propostas_arquivadas_e_nao_privadas=todas_propostas_arquivadas_e_nao_privadas)


@app.route("/likear_proposta", methods=["POST"])
@login_required
def likear_proposta():
    proposta_a_likear = Proposta.query.filter_by(id=request.form.get("id_proposta")).first()
    proposta_a_likear_contador = proposta_a_likear.contador_de_like

    if proposta_a_likear:
        propostas_que_dei_like = current_user.likesPropostas

        if proposta_a_likear in propostas_que_dei_like:
            current_user.likesPropostas.remove(proposta_a_likear)
            proposta_a_likear.contador_de_like = proposta_a_likear_contador - 1
            db.session.commit()
            return Response(json.dumps({ "likeado": False, "numeros_de_like": len(proposta_a_likear.likes) }))
        else:
            current_user.likesPropostas.append(proposta_a_likear)
            proposta_a_likear.contador_de_like = proposta_a_likear_contador + 1
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


@app.route("/participar", methods=["POST"])
@login_required
def participar():
    proposta_que_quero_entrar = Proposta.query.filter_by(id=request.form.get("id_proposta")).first()

    if proposta_que_quero_entrar:
        verificar_se_ja_pediu = Notificacoes_Pedir_para_Participar.query.filter_by(quem_pediu_para_entrar=current_user.apelido, proposta_id=proposta_que_quero_entrar.id).first()

        if verificar_se_ja_pediu:
            return jsonify({"status": 400, "mensagem": "Solicitação já foi previamente enviada"})

        if proposta_que_quero_entrar in current_user.propostas_que_estou:
            return jsonify({"status": 400, "mensagem": "Você já participa desta proposta"})

        gerente_da_proposta = User.query.filter_by(id=proposta_que_quero_entrar.gerente_id).first()

        today = date.today()
        notificacao = Notificacoes_Pedir_para_Participar(quem_pediu_para_entrar=current_user.apelido, quem_pediu_para_entrar_foto=current_user.foto_perfil, titulo_da_proposta=proposta_que_quero_entrar.titulo, gerente_da_proposta=gerente_da_proposta, proposta_id=proposta_que_quero_entrar.id, dia_criacao=today.day, mes_criacao=today.month, ano_criacao=today.year)

        gerente_da_proposta.notificacoes_pedir_para_participar.append(notificacao)

        db.session.commit()

        return jsonify({"status": 200, "mensagem": "Solicitação enviada com sucesso"})
    else:
        return render_template("erro.html", codigo=404, mensagem="ERRO NO SERVER - PROPOSTA NÃO ENCONTRADA")


@app.route("/aprovar_participacao", methods=["POST"])
@login_required
def aprovar_participacao():
    quem_pediu_para_entrar = request.form.get("quem_pediu_para_entrar")
    proposta_id = request.form.get("proposta_id")

    notificacao = Notificacoes_Pedir_para_Participar.query.filter_by(quem_pediu_para_entrar=quem_pediu_para_entrar, proposta_id=proposta_id).first()

    if notificacao:
        proposta = Proposta.query.filter_by(id=proposta_id).first()
        usuario = User.query.filter_by(apelido=quem_pediu_para_entrar).first()

        usuario.propostas_que_estou.append(proposta)

        Notificacoes_Pedir_para_Participar.query.filter_by(quem_pediu_para_entrar=quem_pediu_para_entrar, proposta_id=proposta_id).delete()
        db.session.commit()
        return jsonify({'codigo': 200})
    else:
        return render_template("erro.html", codigo=404, mensagem="ERRO NO SERVER - USUÁRIO NÃO PEDIU PARA PARTICIPAR")

    
@app.route("/recusar_participacao", methods=["POST"])
@login_required
def recusar_participacao():
    quem_pediu_para_entrar = request.form.get("quem_pediu_para_entrar")
    proposta_id = request.form.get("proposta_id")

    notificacao = Notificacoes_Pedir_para_Participar.query.filter_by(quem_pediu_para_entrar=quem_pediu_para_entrar, proposta_id=proposta_id).first()

    if notificacao:
        db.session.delete(notificacao)
        db.session.commit()
        return jsonify({'codigo': 200})
    else:
        return render_template("erro.html", codigo=404, mensagem="ERRO NO SERVER - USUÁRIO NÃO PEDIU PARA PARTICIPAR")


@app.route("/editar_proposta", methods=["GET", "POST"])
@login_required
def editar_proposta():
    formDeProposta = FormDeProposta()

    # Se for post
    if formDeProposta.validate_on_submit():
        proposta_id = request.form.get("proposta_id")
        proposta_a_editar = Proposta.query.filter_by(id=proposta_id).first()

        proposta_a_editar.titulo = formDeProposta.titulo.data
        proposta_a_editar.descricao = formDeProposta.descricao.data
        proposta_a_editar.restricao_idade = formDeProposta.restricao_idade.data

        if request.form.get("privado") == "on":
            proposta_a_editar.privado = True
        else:
            proposta_a_editar.privado = False

        if request.form.get("arquivado") == "on":
            proposta_a_editar.arquivado = True
        else:
            proposta_a_editar.arquivado = False

        membros_antigos = proposta_a_editar.membros

        # Remover todos menos o gerente se o campo de membros vier vazio
        if not request.form.getlist("membros"):
            for membro_antigo in membros_antigos:
                if not membro_antigo == current_user:
                    membro_antigo.propostas_que_estou.remove(proposta_a_editar)
            db.session.commit()
            return redirect(url_for("index"))

        # Remover somentes os que foram removidos da form
        for membro_antigo in membros_antigos:
            if not membro_antigo.apelido in request.form.getlist("membros"):
                membro_antigo.propostas_que_estou.remove(proposta_a_editar)
        
        # Adicionar os que foram adicionados na form
        for membro_novo in request.form.getlist("membros"):
            user = User.query.filter_by(apelido=membro_novo).first()
            if not user in membros_antigos:
                user.propostas_que_estou.append(proposta_a_editar)

        db.session.commit()
        return redirect(url_for("index"))
    
    proposta_id = request.args.get("proposta_id")
    proposta_a_editar = Proposta.query.filter_by(id=proposta_id).first()

    if not proposta_a_editar.gerente_id == current_user.id:
        return render_template("erro.html", codigo=405, mensagem="NÃO AUTORIZADO - VOCÊ NÃO É GERENTE DESTA PROPOSTA")

    return render_template("editar_proposta.html", proposta_a_editar=proposta_a_editar, formDeProposta=formDeProposta, user=current_user)


@app.route("/deletar_proposta", methods=["GET", "POST"])
@login_required
def deletar_proposta():
    # Se for post
    if request.method == "POST":
        proposta_id = request.form.get("proposta_id")
        proposta_a_deletar = Proposta.query.filter_by(id=proposta_id)

        proposta_a_deletar.delete()
        db.session.commit()
        return redirect(url_for("index"))

    proposta_id = request.args.get("proposta_id")
    proposta_a_deletar = Proposta.query.filter_by(id=proposta_id).first()

    if not proposta_a_deletar.gerente_id == current_user.id:
        return render_template("erro.html", codigo=405, mensagem="NÃO AUTORIZADO - VOCÊ NÃO É GERENTE DESTA PROPOSTA")

    return render_template("deletar_proposta.html", proposta_a_deletar=proposta_a_deletar, user=current_user)