from flask import Blueprint, request, jsonify, render_template
from libs.sql import *

page = Blueprint('page', __name__)

@page.route('/')
def home():
    return render_template('home.html')

@page.route('/teste', methods=['POST'])
def receber_dados():
    dados = request.json
    objetivo = dados.get("objetivo")
    nome = dados.get("nome")
    email = dados.get("email")
    telefone = dados.get("telefone")
    idade = dados.get("idade")
    altura = dados.get("altura")
    peso = dados.get("peso")
    print(f"Nome: {nome}, Email: {email}, Telefone: {telefone}")


    sqlExecute("""insert into cliente ( objetivo, nome, email, telefone, idade, altura, peso, data_cadastro) 
                    values (%s,%s,%s,%s,%s,%s,%s,NOW())""", (objetivo, nome, email, telefone, idade, altura, peso))

    return jsonify({"status": "sucesso", "mensagem": "Dados recebidos com sucesso"}), 200

