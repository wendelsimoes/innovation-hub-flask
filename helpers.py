from cs50 import SQL
from flask_login import UserMixin

# Configurar banco de dados
db = SQL("sqlite:///innovation-hub.db")

class User(UserMixin):
    id = -1

    def __init__(self, id):
        self.id = db.execute("SELECT id FROM users WHERE id = ?", id)[0]