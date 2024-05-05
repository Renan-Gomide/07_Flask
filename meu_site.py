from flask import Flask, request, render_template, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'chavesecreta'  

# Conexão com o banco de dados MySQL
db_connection = mysql.connector.connect(
    host="monorail.proxy.rlwy.net",
    port=50352,
    user="root",
    password="xcDHGvuxutFYpvNqOmECEmxSrAxNaqoJ",
    database="railway"
)

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

    # Criar uma conexão e cursor
    cursor = db_connection.cursor()

    # Inserir dados na tabela clientes
    sql = "INSERT INTO clientes (nome, email, status, valor, forma_pagamento, parcelas, acesso, mensagem) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (nome, email, status, valor, forma_pagamento, parcelas, acesso, mensagem)
    cursor.execute(sql, val)

    # Commit das mudanças
    db_connection.commit()

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
            cursor = db_connection.cursor()
            sql = "INSERT INTO usuarios (email, senha) VALUES (%s, %s)"
            val = (email, senha)
            cursor.execute(sql, val)
            db_connection.commit()
            print("Inserção bem-sucedida")  
            flash('Usuário criado com sucesso!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Erro ao criar usuário: {str(e)}', 'error')

    return render_template('criar_usuario.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = %s AND senha = %s", (email, senha))
        user = cursor.fetchone()
        cursor.close()
        if user:
            return render_template('logado.html')
        else:
            error = 'Usuário ou senha incorretos'
    return render_template('login.html', error=error)

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    data = request.json
    processar_webhook(data)
    return 'Webhook received', 200

if __name__ == '__main__':
    app.run(debug=True)
