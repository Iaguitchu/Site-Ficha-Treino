from flask import Blueprint, request, jsonify, render_template, current_app
from libs.sql import *
from flask_mail import Message

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

    # Salva no banco de dados
    sqlExecute("""insert into cliente ( objetivo, nome, email, telefone, idade, altura, peso, data_cadastro) 
                  values (%s,%s,%s,%s,%s,%s,%s,NOW())""", (objetivo, nome, email, telefone, idade, altura, peso))

    # Acessa `mail` a partir de `current_app.extensions`
    enviar_email_boas_vindas(email, nome)

    return jsonify({"status": "sucesso", "mensagem": "Dados recebidos com sucesso"}), 200

def enviar_email_boas_vindas(email_destinatario, nome_usuario):
    msg = Message('Bem-vindo ao FitTrack!', recipients=[email_destinatario])
    msg.body = f"Olá {nome_usuario}, obrigado por se registrar no FitTrack! Vamos começar sua jornada de saúde e bem-estar."
    try:
        # Envia o e-mail usando `current_app.extensions`
        current_app.extensions['mail'].send(msg)
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
