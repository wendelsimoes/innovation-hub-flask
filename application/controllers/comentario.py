from application import app, db
from flask_login import login_required, current_user
from application.models.comentario import Comentario
from flask import request, Response, render_template
import json


@app.route("/likear_comentario", methods=["POST"])
@login_required
def likear_comentario():
    comentario_a_likear = Comentario.query.filter_by(id=request.form.get("id_comentario")).first()

    if comentario_a_likear:
        comentarios_que_dei_like = current_user.likes

        if comentario_a_likear in comentarios_que_dei_like:
            comentario_a_likear.likes.remove(current_user)
            db.session.commit()
            return Response(json.dumps({ "likeado": False, "numeros_de_like": len(comentario_a_likear.likes) }))
        else:
            comentario_a_likear.likes.append(current_user)
            db.session.commit()
            return Response(json.dumps({ "likeado": True, "numeros_de_like": len(comentario_a_likear.likes) }))
    else:
        return render_template("erro.html", codigo=404, mensagem="ERRO NO SERVER - COMENTARIO NÃO ENCONTRADO")