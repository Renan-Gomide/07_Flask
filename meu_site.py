from flask import Flask, request, render_template, redirect, url_for, flash
import requests
import json

app = Flask(__name__)
app.secret_key = 'chavesecreta'

# Configurações do Firebase
DATABASE_URL = 'https://hashtag-a1c92-default-rtdb.firebaseio.com/'

def processar_webhook(data):
    nome = data.get('nome')
    email = data.get('email')
    status = data.get('status')
    valor = data.get('valor')
    forma_pagamento = data.get('forma_pagamento')
    parcelas = data.get('parcelas')
    acesso = ''
    mensagem = ''

    if status == 'aprovado':
        acesso = 'liberado'
        mensagem = 'Bem-vindo ao curso!'
    elif status == 'recusado':
        acesso = 'negado'
        mensagem = 'Pagamento recusado'
    elif status == 'reembolsado':
        acesso = 'negado'
        mensagem = ''

    # Montar os dados para serem enviados ao Firebase
    data = {
        'nome': nome,
        'email': email,
        'status': status,
        'valor': valor,
        'forma_pagamento': forma_pagamento,
        'parcelas': parcelas,
        'acesso': acesso,
        'mensagem': mensagem
    }

    # Enviar uma solicitação POST para adicionar os dados ao Firebase Realtime Database
    response = requests.post(f"{DATABASE_URL}/clientes.json", json=data)

    if response.status_code == 200:
        print("Dados inseridos com sucesso no Firebase.")
    else:
        print(f"Erro ao inserir dados no Firebase: {response.text}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/criar_usuario', methods=['GET', 'POST'])
def criar_usuario():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        print("Dados do formulário:", email, senha)

        try:
            data = {
                'email': email,
                'senha': senha
            }

            response = requests.post(f"{DATABASE_URL}/usuarios.json", json=data)

            if response.status_code == 200:
                print("Usuário criado com sucesso no Firebase.")
                flash('Usuário criado com sucesso!', 'success')
                return redirect(url_for('index'))
            else:
                print(f"Erro ao criar usuário no Firebase: {response.text}")
                flash('Erro ao criar usuário.', 'error')
        except Exception as e:
            flash(f'Erro ao criar usuário: {str(e)}', 'error')

    return render_template('criar_usuario.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        print("Dados recebidos no formulário de login:", email, senha)  # Log de depuração

        # Faz a solicitação GET para obter os usuários com o email correspondente
        response = requests.get(f"{DATABASE_URL}/usuarios.json?orderBy=\"email\"&equalTo=\"{email}\"")

        # Verifica se a resposta foi bem-sucedida e se há dados retornados
        if response.status_code == 200:
            users = response.json()
            print("Dados retornados do Firebase:", users)  # Log de depuração
            if users:
                for key, user in users.items():
                    # Verifica se a senha corresponde à senha fornecida
                    if 'senha' in user and user['senha'] == senha:
                        return render_template('logado.html', user_data=user)
                    else:
                        error = 'Senha incorreta'
            else:
                error = 'Usuário não encontrado'
        else:
            error = 'Erro ao buscar usuário no Firebase'
            print("Erro ao buscar usuário no Firebase:", response.text)  # Log de depuração

    return render_template('login.html', error=error)

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    data = request.json
    processar_webhook(data)
    return 'Webhook received', 200

if __name__ == '__main__':
    app.run(debug=True)
