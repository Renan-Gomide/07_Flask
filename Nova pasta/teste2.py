from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dados de usuários (apenas para fins de demonstração, em um cenário real, use um banco de dados)
users = {'user1': 'password1', 'user2': 'password2'}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username] == password:
            # Autenticação bem-sucedida, redirecionar para a página inicial, por exemplo
            return redirect(url_for('index'))
        else:
            # Autenticação falhou, exibir mensagem de erro na tela de login
            return render_template('login.html', error='Usuário ou senha inválidos.')
    
    # Se o método for GET, exibir o formulário de login
    return render_template('login.html', error=None)

@app.route('/')
def index():
    return 'Página inicial'

if __name__ == '__main__':
    app.run(debug=True)
