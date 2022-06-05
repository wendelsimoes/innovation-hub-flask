from faker import Faker
from random import seed, randint
from werkzeug.security import generate_password_hash
from application import db
from application.models.user import User
from application.models.proposta import Proposta
from application.models.categoria import Categoria
from application.models.comentario import Comentario
import requests


def get_foto_perfil_aleatoria():
    try:
        response = requests.get("https://randomuser.me/api/")
        response.raise_for_status()
    except requests.RequestException:
        return None

    try:
        dados = response.json()
        return dados["results"][0]["picture"]["large"]
    except (KeyError, TypeError, ValueError):
        return None


tipo_proposta = ['Projeto', 'Ideia', 'Problema']

categorias = [
    "Arte e Cultura",
    "Música e Entretenimento",
    "Automoveis e Veiculos",
    "Informatica e Eletrônica",
    "Educação",
    "Vida",
    "Família",
    "Negócios e Empreendedorismo",
    "Culinária e Gastronomia",
    "Saúde e Bem Estar",
    "Esporte",
    "Viagem e Turismo",
    "Economia e Finanças",
    "Política e Mundo",
    "Ciência e Tecnologia",
    "Trabalho e Carreira",
    "Psicologia e Sociedade",
    "Meio Ambiente"
]

def semear_banco():
    fake = Faker()
    seed(1)

    print("SEMEANDO PROPOSTAS...")
    novas_propostas = []
    for i in range(200):
        nova_proposta = Proposta(titulo=fake.bs(), descricao=fake.paragraph(nb_sentences=4, variable_nb_sentences=False), restricao_idade=randint(0, 12), arquivado=fake.boolean(chance_of_getting_true=25), dia_criacao=randint(1, 28), mes_criacao=randint(1, 12), ano_criacao=randint(2000, 2022), privado=fake.boolean(chance_of_getting_true=25), tipo_proposta=fake.word(ext_word_list=tipo_proposta))

        novas_propostas.append(nova_proposta)

        db.session.add(nova_proposta)


    print("SEMEANDO USUÁRIOS...")
    novos_usuarios = []
    for i in range(100):
        apelido = fake.user_name()

        novo_usuario = User(email=fake.email(), nome=fake.first_name(), sobrenome=fake.last_name(), dia_nascimento=randint(1, 28), mes_nascimento=randint(1, 12), ano_nascimento=randint(1980, 2010), apelido=apelido, senha_encriptada=generate_password_hash(apelido), foto_perfil=get_foto_perfil_aleatoria())

        novos_usuarios.append(novo_usuario)

        for proposta in novas_propostas:
            # Definir likeado
            if randint(1, 4) == 3:
                proposta.likes.append(novo_usuario)
            # Definir membros
            if randint(1, 8) == 3:
                proposta.membros.append(novo_usuario)
            if randint(1, 12) == 3:
                proposta.favoritadores.append(novo_usuario)

        db.session.add(novo_usuario)

    db.session.commit()
    
    for proposta in novas_propostas:
        user = User.query.filter_by(id=randint(1, 100)).first()
        # Definir gerente
        proposta.gerente_de_projeto == user
        proposta.gerente_id == user.id
        # Definir count de like
        proposta.contador_de_like = len(proposta.likes)

    print("SEMEANDO CATEGORIAS...")
    for i in range(1000):
        random_proposta = novas_propostas[randint(0, 199)]
        random_categoria = randint(0, 17)
        nova_categoria = Categoria(nome=categorias[random_categoria], valor=random_categoria)

        contem = False
        categorias_da_proposta = random_proposta.categorias
        for categoria in categorias_da_proposta:
            if categoria.nome == nova_categoria.nome:
                contem = True
        
        if not contem:
            nova_categoria.proposta = random_proposta

        db.session.add(nova_categoria)

    
    print("SEMEANDO COMENTARIOS...")
    novos_comentarios = []
    for i in range(2000):
        random_usuario = novos_usuarios[randint(0, 99)]
        random_proposta = novas_propostas[randint(0, 199)]

        novo_comentario = Comentario(texto_comentario=fake.paragraph(nb_sentences=4, variable_nb_sentences=False), dia_criacao=randint(1, 28), mes_criacao=randint(1, 12), ano_criacao=randint(2000, 2022), dono_do_comentario=random_usuario.apelido, proposta_id=random_proposta.id, user=random_usuario, proposta=random_proposta)

        random_proposta.comentarios.append(novo_comentario)

        for user in novos_usuarios:
            if randint(1, 3) == 2:
                novo_comentario.likes.append(user)
        
        novo_comentario.contador_de_like = len(novo_comentario.likes)

        db.session.add(novo_comentario)

    db.session.commit()