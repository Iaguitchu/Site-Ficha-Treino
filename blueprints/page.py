from flask import Blueprint, request, jsonify, render_template

page = Blueprint('page', __name__)

@page.route('/')
def home():
    return render_template('home.html')

@page.route('/teste', methods=['POST'])
def receber_dados():
    dados = request.json
    nome = dados.get("nome")
    email = dados.get("email")
    telefone = dados.get("telefone")
    print(f"Nome: {nome}, Email: {email}, Telefone: {telefone}")
    return jsonify({"status": "sucesso", "mensagem": "Dados recebidos com sucesso"}), 200
