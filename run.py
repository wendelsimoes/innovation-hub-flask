from application import app
from application import db

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

# Para rodar o programa:
# Tenha o python 3 instaldo em sua maquina
# No Windows execute "py -3 -m venv venv"
# No Windows execute "venv\Scripts\activate"
# Se der erro de segurança na execução de scripts siga os seguintes passos:
    # Abra o Windows Powershell
    # Execute "Set-ExecutionPolicy RemoteSigned"
    # Escreva "yes"
# Execute "pip install -r requirements.txt"
# Execute "py .\run.py"