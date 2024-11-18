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
    alimento = dados.get("alimento")
    
    print(f"Nome: {nome}, Email: {email}, alimento{alimento}")

    # Salva no banco de dados
    sqlExecute("""insert into cliente ( objetivo, nome, email, idade, altura, peso, data_cadastro) 
                  values (%s,%s,%s,%s,%s,%s,NOW())""", (objetivo, nome, email, idade, altura, peso))
    
    # Gera o plano de treino e dieta
    plano = gerar_plano_treino_dieta(nome, idade, altura, peso, objetivo, alimento)

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

def gerar_plano_treino_dieta(nome, idade, altura, peso, objetivo, alimento):
    # Parte 1: Calcular TMB
    prompt_tmb = f"Calcule a taxa metabólica basal (TMB) para {nome}, com {idade} anos, {peso} kg, e {altura} cm de altura. Forneça apenas o valor do resultado, sem o cálculo detalhado."

    # Parte 2: Plano de Treino
    prompt_treino = f"""
    Crie um plano de treino de hipertrofia focado em {objetivo} para {nome}, com base no Basal + 300 kcal. O treino deve ser dividido precisa ser dividido desse jeito que vou passar.
    
    Escolha 4 exercicios para costas dessa lista que passei, e 3 para posteriors:
    - Segunda-feira: Costas:
        (Remada Curvada Pronada, Remada Curvada Supinada, Barra Fixa, Puxada alta, Pulldown com corda, remada sentado, Remada Unilateral (serrote)
    
    Posterior de ombro:
        Peck deck invertido
    
    Posterior de cocha:
        (Mesa flexora, cadeira flexora, stiff, elevação pélvica(pode ser no smith))
    
    
    
    Escolha 4 exercicio de peito e coloque o exercicio de panturrilha no começo do treino
    - Terça-feira: Peito
        (supino inclinado com halteres ou articulado, supino reto com barra, packdeck, voador, flexão 60 rep 6x10, cross-over declinado)
    
    Panturrilha:
        (panturrilha no smith com degrau 5x10 15s de descanso)
    
    
    
    - Quarta-feira: Descanso
    
    
    
    Escolha 4 exercicio de quadríceps e coloque pra fazer panturrilha no final do treino
    - Quinta-feira: Pernas
        (agachamento livre ou smith com pés alinhados com tronco, leg-press, cadeira extensora, 5 min passada, bulgaro, afundo)
    
    Panturrilha:
        Gêmeos em pé 5x12 (pesado, 2s alongando)

    
    
    Pode passar esses exatos exercicios nessa ordem
    - Sexta-feira: Braços
        (Rosca Direta, Triceps com corda polia, Rosca Scott, Triceps com barra na polia, Biceps na polia alta unilateral, Triceps na polia unilateral, Biceps no banco 45 martelo simultaneo, triceps testa com barra W)
    

    - Sábado: Ombros
        (Desenvolvimento com halteres + Elevação frontal com barra, Elevação lateral com halter drop set 3x10-8-6, Elevação lateral na polia, Encolhimento com Barra ) 
    
    
    - Domingo: Descanso

    Todos os exercícios devem ser descritos com séries e repetições focadas em hipertrofia, com preferência por equipamentos de academia como halteres e barras.
    Não faça distinção entre iniciantes e avançados. O treino deve ser um plano padrão, diretamente aplicável ao usuário.
    """

    # Parte 3: Plano de Dieta
    if alimento:
        restricao_alimentos = f"Evite incluir os seguintes alimentos na dieta: {alimento}."
    else:
        restricao_alimentos = ""

    prompt_dieta = f"""
    Elabore um plano de dieta para {nome} com o objetivo de {objetivo}, dividido em 5 refeições: café da manhã, almoço, lanche da tarde, jantar e ceia.
    - Cada refeição deve especificar a quantidade de alimentos em gramas (g), ao invés de colheres ou porções, e dar mais opções de proteína (ex: frango, filé mignon, tilápia, filé mignon suíno).
    - Inclua alimentos típicos da dieta brasileira e fáceis de encontrar no Brasil, limite o feijão para até no maximo 70g.
    - Adicione uma observação que saladas e vegetais são à vontade, sem limite de quantidade.
    - Adicione uma observação que as proteínas pode ser frango, patinho, filé mignon, tilápia ou filé mignon suíno
    - Coloque sempre carboidratos na dieta, nem que seja pouco, mas nunca zere os carboidratos
    - Na janta e almoço smepre terá arroz branco
    {restricao_alimentos}
    """

    try:
        # Geração de cada parte
        response_tmb = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_tmb}],
            max_tokens=200,
            temperature=0.7
        )
        
        response_treino = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_treino}],
            max_tokens=500,
            temperature=0.7
        )
        
        response_dieta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_dieta}],
            max_tokens=500,
            temperature=0.7
        )
        
        # Combina as partes
        tmb_text = response_tmb.choices[0].message["content"]
        treino_text = response_treino.choices[0].message["content"]
        dieta_text = response_dieta.choices[0].message["content"]
        
        # Texto final
        return f"1. Taxa Metabólica Basal (TMB):\n{tmb_text}\n\n2. Ficha de Treino:\n{treino_text}\n\n3. Plano de Dieta:\n{dieta_text}"

    except Exception as e:
        print(f"Erro ao acessar OpenAI: {e}")
        return "Não foi possível gerar o plano de treino e dieta no momento."



