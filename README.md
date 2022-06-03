## PARA RODAR O PROGRAMA:
### 1. Va no arquivo __init_.py e edite a string de conexão para o seu MySql
### 2. Tenha o python 3 instaldo em sua maquina
### 3. Abra o terminal na pasta do projeto
### 4. No Windows execute "py -3 -m venv venv"
### 5. No Windows execute "venv\Scripts\activate"
### 6. Se der erro de segurança na execução de scripts siga os seguintes passos:
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. Abra o Windows Powershell
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. Execute "Set-ExecutionPolicy RemoteSigned"
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3. Execute "yes"
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4. Volte ao passo 4
### 7. Execute "pip install -r requirements.txt"
### 8. Na pasta primeira do projeto use o comando "$env:FLASK_APP = "application/main.py""
### 9. Execute "flask run"
### 10. Se não tiver um innovation-hub-flask.db na pasta application e der erro:
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. Na pasta primeira do projeto use o comando "py"
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. Execute "from application import db"
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3. Execute "db.create_all()"
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4. Volte ao passo 8