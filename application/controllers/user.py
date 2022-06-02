from application import app
from application.models.user import User
from flask import Response, request
import json
from flask_login import current_user


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