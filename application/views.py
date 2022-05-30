from flask import flash, redirect, render_template, request
from flask_login import login_required, login_user, logout_user, login_manager, current_user
from application import app, login_manager, db
from application.forms import FormDeLogin, FormDeRegistro, FormDeProposta
from application.models import User, Proposta, Categoria


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


# Feed
@app.route("/feed")
@login_required
def feed():
    formDeProposta = FormDeProposta()
    return render_template("feed.html", formDeProposta=formDeProposta, categorias=categorias, tipo_proposta=tipo_proposta, user=current_user)


# Postar proposta
@app.route("/postar", methods=["POST"])
@login_required
def postar():
    formDeProposta = FormDeProposta()

    if not formDeProposta.validate_on_submit():
        return render_template("feed.html", formDeProposta=formDeProposta, categorias=categorias, tipo_proposta=tipo_proposta, user=current_user)
    
    if not int(request.form.get("tipo_proposta")) in tipo_proposta.values():
        return render_template("erro.html", codigo=500, mensagem="ERRO NO SERVER - TENTE NOVAMENTE")

    for categoria_valor in request.form.getlist("categorias"):
        if not int(categoria_valor) in categorias.values():
            return render_template("erro.html", codigo=500, mensagem="ERRO NO SERVER - TENTE NOVAMENTE")

    privado = True if request.form.get("privado") == "on" else False

    nova_proposta = Proposta(titulo=formDeProposta.titulo.data, descricao=formDeProposta.descricao.data, restricao_idade=formDeProposta.restricao_idade.data, privado=privado)
    db.session.add(nova_proposta)
    db.session.commit()

    # Lidar com lista de categorias e escolha de tipo de proposta
    print(request.form.getlist("categorias"))
    for categoria, valor in categorias.items():
        if str(valor) in request.form.getlist("categorias"):
            nova_categoria = Categoria(nome=categoria, valor=valor, proposta=nova_proposta)
            db.session.add(nova_categoria)

    db.session.commit()
    return redirect("/feed")


# Registrar
@app.route("/registrar", methods=["POST"])
def registrar():
    formDeRegistro = FormDeRegistro()

    if not formDeRegistro.validate_on_submit():
        return render_template("index.html", formDeRegistro=formDeRegistro, formDeLogin=FormDeLogin(), abrirModalDeRegistro=True, abrirModalDeLogin=False)

    novo_usuario = User(formDeRegistro.email.data, formDeRegistro.nome.data, formDeRegistro.sobrenome.data, formDeRegistro.nascimento.data.day, formDeRegistro.nascimento.data.month, formDeRegistro.nascimento.data.year, formDeRegistro.apelido.data, formDeRegistro.senha.data)

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
    return redirect("/")


@app.route("/sair")
def logout():
    # Deslogar qualquer usuário que tenha logado anteriormente
    logout_user()

    return redirect("/")


@login_manager.unauthorized_handler
def unauthorized():
    # Mostrar uma página de erro
    return render_template("erro.html", codigo=403, mensagem="NÃO AUTORIZADO - LOGIN NECESSÁRIO")