from flask import Flask, request, render_template, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'chavesecreta'  # Defina uma chave secreta adequada aqui

# Configurações do banco de dados MySQL
app.config['MYSQL_HOST'] = 'monorail.proxy.rlwy.net'
app.config['MYSQL_PORT'] = 50352
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'xcDHGvuxutFYpvNqOmECEmxSrAxNaqoJ'
app.config['MYSQL_DB'] = 'railway'
mysql = MySQL(app)

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
        mensagem = 'Bem vindo ao curso!'
    elif status == 'recusado':
        acesso = 'negado'
        mensagem = 'Pagamento recusado'
    elif status == 'reembolsado':
        acesso = 'negado'
        mensagem = ''

    # Conectar ao banco de dados
    cur = mysql.connection.cursor()
    # Executar a query para inserir os dados na tabela 'clientes'
    cur.execute("INSERT INTO clientes (nome, email, status, valor, forma_pagamento, parcelas, acesso, mensagem) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                (nome, email, status, valor, forma_pagamento, parcelas, acesso, mensagem))
    # Commit para salvar as mudanças no banco de dados
    mysql.connection.commit()
    # Fechar o cursor
    cur.close()

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bd')
def bd():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios")
    data = cur.fetchall()
    cur.close()
    return str(data)


@app.route('/criar_usuario', methods=['GET', 'POST'])
def criar_usuario():
    if request.method == 'POST':
        # Receber os dados do formulário
        username = request.form['username']
        password = request.form['password']
        print("Dados do formulário:", username, password)  # Depuração
        try:
            # Conectar ao banco de dados
            cur = mysql.connection.cursor()
            # Executar a query para inserir o novo usuário na tabela 'usuarios'
            cur.execute("INSERT INTO usuarios (email, senha) VALUES (%s, %s)", (username, password))
            # Commit para salvar as mudanças no banco de dados
            mysql.connection.commit()
            print("Inserção bem-sucedida")  # Depuração
            # Fechar o cursor
            cur.close()
            # Exibir mensagem de sucesso
            flash('Usuário criado com sucesso!', 'success')
            # Redirecionar para a página inicial após a inserção
            return redirect(url_for('index'))
        except Exception as e:
            # Exibir mensagem de erro
            flash(f'Erro ao criar usuário: {str(e)}', 'error')
    # Se o método for GET, renderizar o template do formulário
    return render_template('criar_usuario.html')

# Rota para login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # Autenticação de login
        username = request.form['username']
        password = request.form['password']
        # Verificar se o usuário e senha estão corretos
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email = %s AND senha = %s", (username, password))
        user = cur.fetchone()
        cur.close()
        if user:
            # Se as credenciais estiverem corretas, redireciona para a página de sucesso
            return render_template('logado.html')
        else:
            # Se as credenciais estiverem incorretas, define a mensagem de erro
            error = 'Usuário ou senha incorretos'
    # Se o método for GET ou se houver erro, exibe o formulário de login com a mensagem de erro
    return render_template('login2.html', error=error)

# Rota para receber webhooks do sistema de pagamento
@app.route('/webhook', methods=['POST'])
def webhook_handler():
    data = request.json
    # Processar o webhook e inserir os dados no banco de dados
    processar_webhook(data)
    return 'Webhook received', 200


# Rota para as tratativas
@app.route('/tratativas')
def tratativas():
    # Lógica para buscar e exibir tratativas do banco de dados
    # ...
    return 'Tratativas'

if __name__ == '__main__':
    app.run(debug=True)
