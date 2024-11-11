from flask import Blueprint, request, jsonify, render_template, current_app
from libs.sql import *
from flask_mail import Message
import openai
import os

page = Blueprint('page', __name__)

openai.api_key = os.environ.get("OPENAI_KEY")


@page.route('/')
def home():
    return render_template('home.html')

@page.route('/teste', methods=['POST'])
def receber_dados():
    dados = request.json
    objetivo = dados.get("objetivo")
    nome = dados.get("nome")
    email = dados.get("email")
    idade = dados.get("idade")
    altura = dados.get("altura")
    peso = dados.get("peso")
    
    print(f"Nome: {nome}, Email: {email}")

    # Salva no banco de dados
    sqlExecute("""insert into cliente ( objetivo, nome, email, idade, altura, peso, data_cadastro) 
                  values (%s,%s,%s,%s,%s,%s,NOW())""", (objetivo, nome, email, idade, altura, peso))
    
    # Gera o plano de treino e dieta

    prompt = f"""
    Crie um plano de treino focado em hipertrofia para {nome}, que tem {idade} anos, pesa {peso} kg, mede {altura} cm e deseja {objetivo}. 
    Calcule a taxa metabólica basal (TMB) da pessoa e, com base nisso, elabore um plano de dieta que suporte o ganho muscular ou emagrecimento com base no {objetivo} calórico adequado.
    
    - O plano de treino deve incluir exercícios de musculação com séries e repetições focadas em hipertrofia, preferencialmente utilizando equipamentos de academia, priorize mais exercicos
        com halteres e barra.
    - O plano de dieta deve conter alimentos facil de serem encontrados em mercados com base no que o brasileiro come, dividido em 5 refeições, café da manhã, almoço,
      lanche da tarde, janta e ceia.
    """
    plano = gerar_plano_treino_dieta(prompt)

    # Envia o plano de treino e dieta por e-mail
    enviar_email_boas_vindas(email, nome, plano)

    return jsonify({"status": "sucesso", "mensagem": "Dados recebidos com sucesso"}), 200

def enviar_email_boas_vindas(email_destinatario, nome_usuario, plano_treino_dieta):
    msg = Message('Bem-vindo ao FitTrack!', recipients=[email_destinatario])
    msg.body = (
        f"Olá {nome_usuario}, obrigado por se registrar no FitTrack!\n\n"
        "Aqui está seu plano de treino e dieta personalizado:\n\n"
        f"{plano_treino_dieta}\n\n"
        "Esperamos que isso o ajude a atingir seus objetivos de saúde e bem-estar!"
    )
    try:
        # Envia o e-mail usando `current_app.extensions`
        current_app.extensions['mail'].send(msg)
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

def gerar_plano_treino_dieta(prompt):
    
    messages = [{"role": "user", "content": prompt}]
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=300,
            temperature=3 
        ) 
        
        # Retorna a resposta do ChatGPT
        return response.choices[0].message["content"]
    
    except Exception as e:
        print(f"Erro ao acessar OpenAI: {e}")
        return "Não foi possível gerar o plano de treino e dieta no momento."
    




