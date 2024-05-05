# 1.Configurar o Flask e definir rotas para os webhooks:
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    data = request.json
    # Lógica para tratar o webhook e tomar as ações necessárias
    return 'Webhook received', 200

if __name__ == '__main__':
    app.run(debug=True)

# 2.Lógica para tratar os webhooks:

def process_payment_approved(data):
    email = data['email']
    print(f"Liberar acesso do e-mail: {email}")
    print(f"Enviar mensagem de boas vindas para o email: {email}")

def process_payment_declined(data):
    email = data['email']
    print(f"Enviar mensagem de pagamento recusado para o email: {email}")

def process_refunded(data):
    email = data['email']
    print(f"Tirar acesso do e-mail: {email}")

def process_webhook(data):
    status = data['status']
    if status == 'approved':
        process_payment_approved(data)
    elif status == 'declined':
        process_payment_declined(data)
    elif status == 'refunded':
        process_refunded(data)

    # Salvar registro da tratativa no banco de dados

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    data = request.json
    process_webhook(data)
    return 'Webhook received', 200

# 3.Adicionar autenticação e rota para visualizar tratativas:

from functools import wraps
from flask import request, jsonify

# Função para verificar token de autenticação
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if token != 'uhdfaAADF123':
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

# Rota para visualizar tratativas
@app.route('/tratativas')
@requires_auth
def tratativas():
    # Lógica para buscar e exibir tratativas do banco de dados
    return 'Tratativas'

if __name__ == '__main__':
    app.run(debug=True)
