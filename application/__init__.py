from flask import Flask
from flask_login import LoginManager, login_manager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "chave_secreta"

# Configurar login geral para bloquar acesso de alguma páginas
login_manager = LoginManager()
login_manager.init_app(app)

# Configurar banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///innovation-hub-flask.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

import application.main