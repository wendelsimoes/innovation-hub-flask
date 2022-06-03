from flask import flash, redirect, render_template, request, Response, url_for
from flask_login import login_required, login_user, logout_user, login_manager, current_user
from application import app, login_manager, db
from application.forms import FormDeLogin, FormDeRegistro, FormDeProposta, FormDeConfiguracao

from application.models.user import User
from application.models.proposta import Proposta
from application.models.categoria import Categoria
from application.models.comentario import Comentario
from application.models.notificacoes_pedir_para_participar import Notificacoes_Pedir_para_Participar

from datetime import date
from werkzeug.security import generate_password_hash
import json
from werkzeug.utils import secure_filename
import base64
import os
import cloudinary
import cloudinary.uploader

from application.models.categorias import categorias

from application.models.tipo_proposta import tipo_proposta

cloudinary.config( 
  cloud_name = "dpvpgl0el", 
  api_key = "293558758171612", 
  api_secret = "CIhjIg0vTjEIVo_PJ-LRD8aTiuw" 
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


from application.controllers import home
from application.controllers import user
from application.controllers import feed
from application.controllers import proposta
from application.controllers import comentario


@app.route("/recusar_participacao", methods=["POST"])
@login_required
def recusar_participacao():
    quem_pediu_para_entrar = request.form.get("quem_pediu_para_entrar")
    proposta_id = request.form.get("proposta_id")

    notificacao = Notificacoes_Pedir_para_Participar.query.filter_by(quem_pediu_para_entrar=quem_pediu_para_entrar, proposta_id=proposta_id).first()

    if notificacao:
        Notificacoes_Pedir_para_Participar.query.filter_by(quem_pediu_para_entrar=quem_pediu_para_entrar, proposta_id=proposta_id).delete()
        return Response(json.dumps({'codigo': 200}))
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

        membros_antigos = proposta_a_editar.membro

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


# Registrar
@app.route("/registrar", methods=["POST"])
def registrar():
    formDeRegistro = FormDeRegistro()

    if not formDeRegistro.validate_on_submit():
        return render_template("index.html", formDeRegistro=formDeRegistro, formDeLogin=FormDeLogin(), abrirModalDeRegistro=True, abrirModalDeLogin=False, user=current_user)


    novo_usuario = User(email=formDeRegistro.email.data, nome=formDeRegistro.nome.data, sobrenome=formDeRegistro.sobrenome.data, dia_nascimento=formDeRegistro.nascimento.data.day, mes_nascimento=formDeRegistro.nascimento.data.month, ano_nascimento=formDeRegistro.nascimento.data.year, apelido=formDeRegistro.apelido.data, senha_encriptada=generate_password_hash(formDeRegistro.senha.data), foto_perfil="/static/images/foto-padrao.png")
    
    if formDeRegistro.foto_perfil.data:
        foto_perfil = formDeRegistro.foto_perfil.data
        nome_da_foto = secure_filename(foto_perfil.filename)

        url = cloudinary.uploader.upload(foto_perfil, public_id = f"nome_da_foto_{novo_usuario.apelido}")
        novo_usuario.foto_perfil = url['url']

    db.session.add(novo_usuario)

    db.session.commit()

    return redirect("/")


@app.route("/entrar", methods=["POST"])
def login():
    formDeLogin = FormDeLogin()

    if not formDeLogin.validate_on_submit():
        return render_template("index.html", formDeRegistro=FormDeRegistro(), formDeLogin=formDeLogin, abrirModalDeRegistro=False, abrirModalDeLogin=True, user=current_user)
    
    # Logar
    user = User.query.filter_by(apelido=formDeLogin.apelido.data).first()

    if request.form.get("lembrar_de_mim") == "on":
        login_user(user, remember=True)
    else:
        login_user(user)
        
    # Redirect user to home page
    return redirect(url_for("index"))

@app.route("/configuracoes_usuario", methods=["GET", "POST"])
def configuracoes_usuario():
    formDeConfiguracao = FormDeConfiguracao()

    if formDeConfiguracao.validate_on_submit():
        current_user.email = formDeConfiguracao.email.data
        current_user.senha_encriptada = generate_password_hash(formDeConfiguracao.senha.data)

        if formDeConfiguracao.foto_perfil.data:
            foto_perfil = formDeConfiguracao.foto_perfil.data
            nome_da_foto = secure_filename(foto_perfil.filename)

            url = cloudinary.uploader.upload(foto_perfil, public_id = f"nome_da_foto_{current_user.apelido}")
            current_user.foto_perfil = url['url']

        db.session.commit()
        return redirect(url_for("index"))
    
    return render_template("configuracoes_usuario.html", user=current_user, formDeConfiguracao=formDeConfiguracao)


@app.route("/sair")
def logout():
    # Deslogar qualquer usuário que tenha logado anteriormente
    logout_user()

    return redirect(url_for("index"))


@login_manager.unauthorized_handler
def unauthorized():
    # Mostrar uma página de erro
    return render_template("erro.html", codigo=403, mensagem="NÃO AUTORIZADO - LOGIN NECESSÁRIO")


db.create_all()