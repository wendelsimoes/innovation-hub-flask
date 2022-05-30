from flask import flash, redirect, render_template, request, Response, url_for
from flask_login import login_required, login_user, logout_user, login_manager, current_user
from application import app, login_manager, db
from application.forms import FormDeLogin, FormDeRegistro, FormDeProposta, FormDeComentario
from application.models import User, Proposta, Categoria, Comentario
from datetime import date
from werkzeug.security import generate_password_hash
import json


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
        user = User.query.filter_by(apelido=apelido).first()
        if user:
            return Response(json.dumps({"status": 200, "mensagem": user.apelido}), mimetype="application\json")
        else:
            return Response(json.dumps({"status": 404, "mensagem": "Usuário não encontrado"}), mimetype="application\json")
    else:
        return Response(json.dumps({"status": 404, "mensagem": "Deve adicionar um apelido"}), mimetype="application\json")


# Feed / Postar proposta
@app.route("/feed", methods=["GET", "POST"])
@login_required
def feed():
    formDeProposta = FormDeProposta()
    formDeComentario = FormDeComentario()

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
    return render_template("postar.html", formDeProposta=formDeProposta, categorias=categorias, tipo_proposta=tipo_proposta, user=current_user, todas_propostas_nao_privadas=todas_propostas_nao_privadas, formDeComentario=formDeComentario)


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
        todos_comentarios_da_proposta = proposta_a_comentar.comentarios

        todos_comentarios_da_proposta_dict = []

        for comentario in todos_comentarios_da_proposta:
            todos_comentarios_da_proposta_dict.append({
                "id": comentario.id,
                "texto_comentario": comentario.texto_comentario,
                "dia_criacao": comentario.dia_criacao,
                "mes_criacao": comentario.mes_criacao,
                "ano_criacao": comentario.ano_criacao,
                "dono_do_comentario": comentario.dono_do_comentario
            })

        return Response(json.dumps({"status": 200, "info": todos_comentarios_da_proposta_dict}), mimetype="application\json")
    else:
        return render_template("erro.html", codigo=404, mensagem="ERRO NO SERVER - PROPOSTA NÃO ENCONTRADA")



# Registrar
@app.route("/registrar", methods=["POST"])
def registrar():
    formDeRegistro = FormDeRegistro()

    if not formDeRegistro.validate_on_submit():
        return render_template("index.html", formDeRegistro=formDeRegistro, formDeLogin=FormDeLogin(), abrirModalDeRegistro=True, abrirModalDeLogin=False, user=current_user)

    novo_usuario = User(email=formDeRegistro.email.data, nome=formDeRegistro.nome.data, sobrenome=formDeRegistro.sobrenome.data, dia_nascimento=formDeRegistro.nascimento.data.day, mes_nascimento=formDeRegistro.nascimento.data.month, ano_nascimento=formDeRegistro.nascimento.data.year, apelido=formDeRegistro.apelido.data, senha_encriptada=generate_password_hash(formDeRegistro.senha.data))

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