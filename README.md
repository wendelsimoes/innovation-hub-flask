## PARA RODAR O PROGRAMA:
### 1. Tenha o python 3 instaldo em sua maquina
### 2. Abra o terminal na pasta do projeto
### 3. No Windows execute "py -3 -m venv venv"
### 4. No Windows execute "venv\Scripts\activate"
### 5. Se der erro de segurança na execução de scripts siga os seguintes passos:
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. Abra o Windows Powershell
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. Execute "Set-ExecutionPolicy RemoteSigned"
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3. Execute "yes"
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4. Volte ao passo 4
### 6. Execute "pip install -r requirements.txt"
### 7. Na pasta primeira do projeto use o comando "$env:FLASK_APP = "application/main.py""
### 8. Va até o arquivo __init_ e confira qual banco esta usando
### 9. Se estiver usando o MySQL crie um banco vazio chamado "innovation-hub-flask" 
### 9. Execute "flask run"