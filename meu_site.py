from flask import Flask, request, render_template, redirect, url_for, flash
import pandas as pd

app = Flask(__name__)
app.secret_key = 'chavesecreta'

# DataFrame para armazenar os usuários
usuarios = pd.DataFrame(columns=['email', 'senha'])
# DataFrame para armazenar os clientes
clientes = pd.DataFrame(columns=['Nome', 'Email', 'Status', 'Valor', 'Forma_Pagamento', 'Parcelas', 'Acesso', 'Mensagem'])

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

    # Adicionar os dados ao DataFrame de clientes
    global clientes
    clientes = clientes.append({
        'Nome': nome,
        'Email': email,
        'Status': status,
        'Valor': valor,
        'Forma_Pagamento': forma_pagamento,
        'Parcelas': parcelas,
        'Acesso': acesso,
        'Mensagem': mensagem
    }, ignore_index=True)

@app.route('/')
def index():
    return render_template('index.html')

usuarios = pd.DataFrame(columns=['email', 'senha'])

@app.route('/criar_usuario', methods=['GET', 'POST'])
def criar_usuario():
    global usuarios
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        print("Dados do formulário:", email, senha)

        # Verifica se o email já está cadastrado
        if email in usuarios['email'].values:
            flash('Este email já está cadastrado!', 'error')
        else:
            # Adiciona o novo usuário ao DataFrame de usuarios
            usuarios = pd.concat([usuarios, pd.DataFrame({'email': [email], 'senha': [senha]})], ignore_index=True)
            flash('Usuário criado com sucesso!', 'success')
            return redirect(url_for('index'))

    return render_template('criar_usuario.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        print("Dados recebidos no formulário de login:", email, senha)  # Log de depuração

        # Verifica se o email está cadastrado e se a senha corresponde
        if email in usuarios['email'].values and senha == usuarios.loc[usuarios['email'] == email, 'senha'].values[0]:
            return render_template('logado.html', clientes=clientes)
        else:
            error = 'Email ou senha incorretos'

    return render_template('login.html', error=error)

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    data = request.json
    processar_webhook(data)
    return 'Webhook received', 200

if __name__ == '__main__':
    app.run(debug=True)
