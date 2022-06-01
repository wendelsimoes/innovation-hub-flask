from flask import flash, redirect, render_template, request, Response, url_for
from flask_login import login_required, login_user, logout_user, login_manager, current_user
from application import app, login_manager, db
from application.forms import FormDeLogin, FormDeRegistro, FormDeProposta
from application.models import User, Proposta, Categoria, Comentario, Notificacoes_Pedir_para_Participar
from datetime import date
from werkzeug.security import generate_password_hash
import json
from werkzeug.utils import secure_filename
import base64
import os
import cloudinary
import cloudinary.uploader


# Popular campos de categorias da proposta
categorias = {
    "Arte e Cultura": 0,
    "Música e Entretenimento": 1,
    "Automoveis e Veiculos": 2,
    "Informatica e Eletrônica": 3,
    "Educação": 4,
    "Vida": 5,
    "Família": 6,
    "Negócios e Empreendedorismo": 7,
    "Culinária e Gastronomia": 8,
    "Saúde e Bem Estar": 9,
    "Esporte": 10,
    "Viagem e Turismo": 11,
    "Economia e Finanças": 12,
    "Política e Mundo": 13,
    "Ciência e Tecnologia": 14,
    "Trabalho e Carreira": 15,
    "Psicologia e Sociedade": 16,
    "Meio Ambiente": 17
}

# Popular tipo de proposta
tipo_proposta = {
    "Projeto": 0,
    "Ideia": 1,
    "Problema": 2
}

cloudinary.config( 
  cloud_name = "dpvpgl0el", 
  api_key = "293558758171612", 
  api_secret = "CIhjIg0vTjEIVo_PJ-LRD8aTiuw" 
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


# Página inicial
@app.route("/")
def index():
    formDeRegistro = FormDeRegistro()
    return render_template("index.html", formDeRegistro=formDeRegistro, formDeLogin=FormDeLogin(), abrirModalDeRegistro=False, abrirModalDeLogin=False, user=current_user)


# Autocomplete de membro
@app.route("/todos_usuarios", methods=["GET"])
def todos_usuarios():
    todos_usuarios = User.query.all()
    todos_usuarios_apelidos = []
    for user in todos_usuarios:
        todos_usuarios_apelidos.append(user.apelido)
    return Response(json.dumps(todos_usuarios_apelidos), mimetype="application\json")


# Checar se usuario existe
@app.route("/checar_usuario", methods=["GET"])
def checar_usuario():
    apelido = request.args.get("apelido")
    if apelido:
        if current_user.apelido == apelido:
            return Response(json.dumps({"status": 400, "mensagem": "Você será adicionado automaticamente ao projeto"}), mimetype="application\json")

        user = User.query.filter_by(apelido=apelido).first()
        if user:
            return Response(json.dumps({"status": 200, "mensagem": user.apelido}), mimetype="application\json")
        else:
            return Response(json.dumps({"status": 404, "mensagem": "Usuário não encontrado"}), mimetype="application\json")
    else:
        return Response(json.dumps({"status": 404, "mensagem": "Deve inserir um apelido"}), mimetype="application\json")


# Feed / Postar proposta
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


# Dar like em comentario
@app.route("/likear_comentario", methods=["POST"])
@login_required
def likear_comentario():
    comentario_a_likear = Comentario.query.filter_by(id=request.form.get("id_comentario")).first()

    if comentario_a_likear:
        comentarios_que_dei_like = current_user.comentarios_que_dei_like

        if comentario_a_likear in comentarios_que_dei_like:
            current_user.comentarios_que_dei_like.remove(comentario_a_likear)
            db.session.commit()
            return Response(json.dumps({ "likeado": False, "numeros_de_like": len(comentario_a_likear.likes) }))
        else:
            current_user.comentarios_que_dei_like.append(comentario_a_likear)
            db.session.commit()
            return Response(json.dumps({ "likeado": True, "numeros_de_like": len(comentario_a_likear.likes) }))
    else:
        return render_template("erro.html", codigo=404, mensagem="ERRO NO SERVER - COMENTARIO NÃO ENCONTRADO")


# Dar like em proposta
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


# Favoritar proposta
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


# Comentar
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
        novo_comentario = Comentario(texto_comentario=request.form.get("texto_comentario"), dia_criacao=today.day, mes_criacao=today.month, ano_criacao=today.year, dono_do_comentario=current_user.apelido, user=current_user, proposta=proposta_a_comentar)

        db.session.commit()

        return redirect(url_for("carregar_comentarios", id_proposta=request.form.get("id_proposta")))
    else:
        return render_template("erro.html", codigo=404, mensagem="ERRO NO SERVER - PROPOSTA NÃO ENCONTRADA")


# Pedir para participar
@app.route("/participar", methods=["POST"])
@login_required
def participar():
    proposta_que_quero_entrar = Proposta.query.filter_by(id=request.form.get("id_proposta")).first()

    if proposta_que_quero_entrar:
        verificar_se_ja_pediu = Notificacoes_Pedir_para_Participar.query.filter_by(quem_pediu_para_entrar=current_user.apelido, proposta_id=proposta_que_quero_entrar.id).first()

        if verificar_se_ja_pediu:
            return Response(json.dumps({"status": 400, "mensagem": "Solicitação já foi previamente enviada"}))

        if proposta_que_quero_entrar in current_user.propostas_que_estou:
            return Response(json.dumps({"status": 400, "mensagem": "Você já participa desta proposta"}))

        gerente_da_proposta = User.query.filter_by(id=proposta_que_quero_entrar.gerente_id).first()

        today = date.today()
        notificacao = Notificacoes_Pedir_para_Participar(quem_pediu_para_entrar=current_user.apelido, quem_pediu_para_entrar_foto=current_user.foto_perfil, titulo_da_proposta=proposta_que_quero_entrar.titulo, gerente_da_proposta=gerente_da_proposta, proposta_id=proposta_que_quero_entrar.id, dia_criacao=today.day, mes_criacao=today.month, ano_criacao=today.year)

        gerente_da_proposta.notificacoes_pedir_para_participar.append(notificacao)

        db.session.commit()

        return Response(json.dumps({"status": 200, "mensagem": "Solicitação enviada com sucesso"}))
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
        return Response(json.dumps({'codigo': 200}))
    else:
        return render_template("erro.html", codigo=404, mensagem="ERRO NO SERVER - USUÁRIO NÃO PEDIU PARA PARTICIPAR") 


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


# Carregar comentarios
@app.route("/carregar_comentarios", methods=["GET"])
def carregar_comentarios():
    id_proposta = request.args.get("id_proposta")

    if id_proposta:
        comentarios_da_proposta = Comentario.query.filter_by(proposta_id=id_proposta).all()
        comentarios_que_dei_like = current_user.comentarios_que_dei_like
        
        if len(comentarios_da_proposta) > 0:
            todos_comentarios_da_proposta_array = []

            for comentario in comentarios_da_proposta:
                likeado = False
                if comentario in comentarios_que_dei_like:
                    likeado = True

                todos_comentarios_da_proposta_array.append({
                        "id": comentario.id,
                        "texto_comentario": comentario.texto_comentario,
                        "dia_criacao": comentario.dia_criacao,
                        "mes_criacao": comentario.mes_criacao,
                        "ano_criacao": comentario.ano_criacao,
                        "dono_do_comentario": comentario.dono_do_comentario,
                        "likeado": likeado,
                        "numeros_de_like": len(comentario.likes)
                    })

            return Response(json.dumps(todos_comentarios_da_proposta_array), mimetype="application\json")
        else:
            return Response(json.dumps({"status": 200, "info": "Niguém fez um comentário ainda, que tal ser o primeiro?"}), mimetype="application\json")
    else:
        return render_template("erro.html", codigo=404, mensagem="ERRO NO SERVER - PROPOSTA NÃO ENCONTRADA")


@app.route("/editar_proposta", methods=["GET", "POST"])
def editar_proposta():
    formDeProposta = FormDeProposta()

    # Se for post
    if formDeProposta.validate_on_submit():
        proposta_id = request.form.get("proposta_id")
        proposta_a_editar = Proposta.query.filter_by(id=proposta_id).first()

        proposta_a_editar.titulo = request.form.get("titulo")
        proposta_a_editar.descricao = request.form.get("descricao")
        proposta_a_editar.restricao_idade = request.form.get("restricao_idade")
        proposta_a_editar.privado = request.form.get("privado")

        membros_antigos = proposta_a_editar.membro

        antigos_membros_apelidos  = []
        for membro in membros_antigos:
            antigos_membros_apelidos.append(membro.apelido)

        novos_membros_apelidos = request.form.getlist("membros")

        for membro in antigos_membros_apelidos:
            if not membro in novos_membros_apelidos:
                user = User.query.filter_by(apelido=membro).first()
                user.propostas_que_estou.remove(proposta_a_editar)

        for membro in novos_membros_apelidos:
            if not membro in antigos_membros_apelidos:
                user = User.query.filter_by(apelido=membro).first()
                user.propostas_que_estou.append(proposta_a_editar)

        db.session.commit()
        return redirect(url_for("index"))
    
    proposta_id = request.args.get("proposta_id")
    proposta_a_editar = Proposta.query.filter_by(id=proposta_id).first()

    return render_template("editar_proposta.html", proposta_a_editar=proposta_a_editar, formDeProposta=formDeProposta, user=current_user)


@app.route("/deletar_proposta", methods=["GET", "POST"])
@login_required
def deletar_proposta():
    # Se for post
    if request.method == "POST":
        proposta_id = request.form.get("proposta_id")
        proposta_a_deletar = Proposta.query.filter_by(id=proposta_id)

        if proposta_a_deletar.first().gerente_id == current_user.id:
            proposta_a_deletar.delete()
            db.session.commit()
            return redirect(url_for("index"))
        else:
            render_template("erro.html", codigo=405, mensagem="NÃO AUTORIZADO - VOCÊ NÃO É GERENTE DESTA PROPOSTA")

    proposta_id = request.args.get("proposta_id")
    proposta_a_deletar = Proposta.query.filter_by(id=proposta_id).first()

    return render_template("deletar_proposta.html", proposta_a_deletar=proposta_a_deletar, user=current_user)


# Registrar
@app.route("/registrar", methods=["POST"])
def registrar():
    formDeRegistro = FormDeRegistro()

    if not formDeRegistro.validate_on_submit():
        return render_template("index.html", formDeRegistro=formDeRegistro, formDeLogin=FormDeLogin(), abrirModalDeRegistro=True, abrirModalDeLogin=False, user=current_user)


    novo_usuario = User(email=formDeRegistro.email.data, nome=formDeRegistro.nome.data, sobrenome=formDeRegistro.sobrenome.data, dia_nascimento=formDeRegistro.nascimento.data.day, mes_nascimento=formDeRegistro.nascimento.data.month, ano_nascimento=formDeRegistro.nascimento.data.year, apelido=formDeRegistro.apelido.data, senha_encriptada=generate_password_hash(formDeRegistro.senha.data), foto_perfil="/static/images/foto-padrao.png")
    
    if formDeRegistro.foto_perfil.data:
        print("reached")
        foto_perfil = formDeRegistro.foto_perfil.data
        nome_da_foto = secure_filename(foto_perfil.filename)

        # imagem_em_bytes = base64.b64encode(foto_perfil.read())

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


@app.route("/sair")
def logout():
    # Deslogar qualquer usuário que tenha logado anteriormente
    logout_user()

    return redirect(url_for("index"))


@login_manager.unauthorized_handler
def unauthorized():
    # Mostrar uma página de erro
    return render_template("erro.html", codigo=403, mensagem="NÃO AUTORIZADO - LOGIN NECESSÁRIO")