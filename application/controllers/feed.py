from application import app
from flask_login import login_required, current_user
from application.forms import FormDeProposta
from flask import request, render_template, redirect, url_for, jsonify
from datetime import date
from application.models.proposta import Proposta, PropostaSchema
from application.models.categoria import Categoria
from application import db
from application.models.tipo_proposta import tipo_proposta
from application.models.categorias import categorias
from sqlalchemy.sql.expression import desc
from application.models.user import UserSchema


@app.route("/feed", methods=["GET", "POST"])
@login_required
def feed():
    formDeProposta = FormDeProposta()

    # Se for POST
    if formDeProposta.validate_on_submit():
        if not int(request.form.get("tipo_proposta")) in tipo_proposta.values():
            return render_template("erro.html", codigo=500, mensagem="ERRO NO SERVER - TIPO DE PROPOSTA NÃO ENCONTRADA")

        for categoria_valor in request.form.getlist("categorias"):
            if not int(categoria_valor) in categorias.values():
                return render_template("erro.html", codigo=500, mensagem="ERRO NO SERVER - CATEGORIA NÃO ENCONTRADA")
                
        privado = True if request.form.get("privado") == "on" else False
        tipo_proposta_selecionado = int(request.form.get("tipo_proposta"))
        for tipo_proposta_string, valor in tipo_proposta.items():
            if tipo_proposta_selecionado == valor:
                tipo_proposta_selecionado = tipo_proposta_string
        
        today = date.today()
        nova_proposta = Proposta(titulo=formDeProposta.titulo.data, descricao=formDeProposta.descricao.data, restricao_idade=formDeProposta.restricao_idade.data, arquivado=False, dia_criacao=today.day, mes_criacao=today.month, ano_criacao=today.year, privado=privado, tipo_proposta=tipo_proposta_selecionado, gerente_de_projeto=current_user, contador_de_like=0)
        db.session.add(nova_proposta)
        db.session.commit()

        # Lidar com lista de categorias e escolha de tipo de proposta
        for categoria, valor in categorias.items():
            if str(valor) in request.form.getlist("categorias"):
                nova_categoria = Categoria(nome=categoria, valor=valor, proposta=nova_proposta)
                db.session.add(nova_categoria)
        
        # Lidar com os membros da proposta
        current_user.propostas_que_estou.append(nova_proposta)

        membros = request.form.getlist("membros")
        if len(membros) > 0:
            for membro in membros:
                if not membro == current_user.apelido:
                    user = User.query.filter_by(apelido=membro).first()
                    if user:
                        user.propostas_que_estou.append(nova_proposta)
        db.session.commit()

        return redirect(url_for("feed"))

    # Se for GET
    ordenar = request.args.get("ordenar")
    proposta_schema = PropostaSchema(many=True)
    user_schema = UserSchema()
    if ordenar == "popular":
        todas_propostas_nao_privadas = Proposta.query.order_by(desc(Proposta.contador_de_like)).filter_by(privado=False).all()
        return jsonify({ "propostas": proposta_schema.dump(todas_propostas_nao_privadas), "user": user_schema.dump(current_user) })
    elif ordenar == "recente":
        todas_propostas_nao_privadas = Proposta.query.order_by(desc(Proposta.ano_criacao)).order_by(desc(Proposta.mes_criacao)).order_by(desc(Proposta.dia_criacao)).filter_by(privado=False).all()
        return jsonify({ "propostas": proposta_schema.dump(todas_propostas_nao_privadas), "user": user_schema.dump(current_user) })

    # Setando as propostas ordenadas por recentes como padrão
    todas_propostas_nao_privadas = Proposta.query.order_by(desc(Proposta.ano_criacao)).order_by(desc(Proposta.mes_criacao)).order_by(desc(Proposta.dia_criacao)).filter_by(privado=False).all()

    return render_template("postar.html", formDeProposta=formDeProposta, categorias=categorias, tipo_proposta=tipo_proposta, user=current_user, todas_propostas_nao_privadas=todas_propostas_nao_privadas)