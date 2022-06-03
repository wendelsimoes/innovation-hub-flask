from application import app, db
from application.models.user import User
from flask import Response, request, render_template, redirect
import json
from flask_login import current_user
from application.forms import FormDeRegistro, FormDeLogin, FormDeConfiguracao
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader


cloudinary.config( 
  cloud_name = "dpvpgl0el", 
  api_key = "293558758171612", 
  api_secret = "CIhjIg0vTjEIVo_PJ-LRD8aTiuw" 
)


@app.route("/todos_usuarios", methods=["GET"])
def todos_usuarios():
    todos_usuarios = User.query.all()
    todos_usuarios_apelidos = []
    for user in todos_usuarios:
        todos_usuarios_apelidos.append(user.apelido)
    return Response(json.dumps(todos_usuarios_apelidos), mimetype="application\json")


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

        url = cloudinary.uploader.upload(foto_perfil, public_id = f"foto_de_{novo_usuario.apelido}")
        novo_usuario.foto_perfil = url['url']

    db.session.add(novo_usuario)

    db.session.commit()

    return redirect("/")


@app.route("/configuracoes_usuario", methods=["GET", "POST"])
def configuracoes_usuario():
    formDeConfiguracao = FormDeConfiguracao()

    if formDeConfiguracao.validate_on_submit():
        current_user.email = formDeConfiguracao.email.data
        current_user.senha_encriptada = generate_password_hash(formDeConfiguracao.senha.data)

        if formDeConfiguracao.foto_perfil.data:
            foto_perfil = formDeConfiguracao.foto_perfil.data
            nome_da_foto = secure_filename(foto_perfil.filename)

            url = cloudinary.uploader.upload(foto_perfil, public_id = f"foto_de{current_user.apelido}")
            current_user.foto_perfil = url['url']

        db.session.commit()
        return redirect(url_for("index"))
    
    return render_template("configuracoes_usuario.html", user=current_user, formDeConfiguracao=formDeConfiguracao)