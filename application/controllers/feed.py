from application import app
from flask_login import login_required, current_user
from application.forms import FormDeProposta
from flask import request, render_template, redirect, url_for
from datetime import date
from application.models.proposta import Proposta
from application.models.categoria import Categoria
from application import db

tipo_proposta = {
    "Projeto": 0,
    "Ideia": 1,
    "Problema": 2
}

from application.models.categorias import categorias


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
        nova_proposta = Proposta(titulo=formDeProposta.titulo.data, descricao=formDeProposta.descricao.data, restricao_idade=formDeProposta.restricao_idade.data, arquivado=False, dia_criacao=today.day, mes_criacao=today.month, ano_criacao=today.year, votos=0, privado=privado, tipo_proposta=tipo_proposta_selecionado, gerente_de_projeto=current_user)
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
    todas_propostas_nao_privadas = Proposta.query.filter_by(privado=False).all()

    return render_template("postar.html", formDeProposta=formDeProposta, categorias=categorias, tipo_proposta=tipo_proposta, user=current_user, todas_propostas_nao_privadas=todas_propostas_nao_privadas)