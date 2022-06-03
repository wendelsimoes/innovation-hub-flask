from flask import Flask
from flask_login import LoginManager, login_manager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config["SECRET_KEY"] = "chave_secreta"

login_manager = LoginManager()
login_manager.init_app(app)

# Comente a linha abaixo se for usar o MySQL
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///innovation-hub-flask.db"
# Comente a linha abaixo se for usar o Sqlite
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:021011wd@localhost/innovation-hub-flask"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)