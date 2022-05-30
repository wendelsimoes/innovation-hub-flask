## PARA RODAR O PROGRAMA:
### 1. Tenha o python 3 instaldo em sua maquina
### 2. Abra o terminal na pasta do projeto
### 3. No Windows execute "py -3 -m venv venv"
### 4. No Windows execute "venv\Scripts\activate"
### 5. Se der erro de segurança na execução de scripts siga os seguintes passos:
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. Abra o Windows Powershell
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. Execute "Set-ExecutionPolicy RemoteSigned"
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3. Execute "yes"
### 6. Execute "pip install -r requirements.txt"
### 7. Na pasta primeira do projeto use o comando "$env:FLASK_APP = "application/views.py""
### 8. Execute "flask run"
### 9. Se não tiver um innovation-hub-flask.db na pasta application e der erro:
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. Na pasta primeira do projeto use o comando "py"
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. Execute "from application import db"
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3. Execute "db.create_all()"