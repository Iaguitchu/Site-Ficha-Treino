from flask import Blueprint, request, jsonify, render_template, current_app
from libs.sql import *
from flask_mail import Message
import openai
import os
from fpdf import FPDF


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
    # sexo = dados.get("sexo")
    
    print(f"Nome: {nome}, Email: {email}, Alimento: {alimento}")

    # Salva no banco de dados
    sqlExecute("""insert into cliente ( objetivo, nome, email, idade, altura, peso, data_cadastro) 
                  values (%s,%s,%s,%s,%s,%s,NOW())""", (objetivo, nome, email, idade, altura, peso))
    
    # basal = calcular_basal(sexo, peso, altura, idade)
    
    # Gera o plano de treino e dieta
    plano = gerar_plano_treino_dieta(nome, idade, objetivo, alimento)

    # Nome do arquivo PDF
    nome_arquivo_pdf = f"Plano_{nome.replace(' ', '_')}.pdf"

    

    # Gera o PDF
    if gerar_pdf(nome_arquivo_pdf, nome, plano):
        print(f"PDF gerado: {nome_arquivo_pdf}")

    # Envia o plano por e-mail com o PDF anexado
    enviar_email_boas_vindas(email, nome, plano, nome_arquivo_pdf)

    return jsonify({"status": "sucesso", "mensagem": "Dados recebidos com sucesso"}), 200

def calcular_basal(sexo, peso, altura, idade):
   
    if sexo.lower() == "masculino":
        # Fórmula para homens
        tmb = 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * idade)
    elif sexo.lower() == "feminino":
        # Fórmula para mulheres
        tmb = 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * idade)

    return round(tmb, 2)



def enviar_email_boas_vindas(email_destinatario, nome_usuario, plano_treino_dieta, arquivo_pdf):
    msg = Message('Bem-vindo ao FitTrack!', recipients=[email_destinatario])
    msg.body = (
        f"Olá {nome_usuario}, obrigado por se registrar no FitTrack!\n\n"
        "Aqui está seu plano de treino e dieta personalizado em anexo.\n\n"
        "Esperamos que isso o ajude a atingir seus objetivos de saúde e bem-estar!"
    )
    try:
        # Anexa o arquivo PDF
        with open(arquivo_pdf, "rb") as pdf_file:
            msg.attach(f"{arquivo_pdf}", "application/pdf", pdf_file.read())

        # Envia o e-mail
        current_app.extensions['mail'].send(msg)
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

def gerar_plano_treino_dieta(nome, idade, objetivo, alimento):


    dados_exemplo = {
    "treino_a": {
        "exercicios_costas": {
            1: "Remada Curvada Pronada",
            2: "Remada Curvada Supinada",
            3: "Barra Fixa",
            4: "Puxada alta",
            5: "Pulldown com corda segure",
            6: "Remada sentado",
            7: "Remada Unilateral (serrote)",
            8: "Remada com Halteres Banco 45º",
        },
        "repeticoes_costas": {
            1: "1x12 2x20 a cada 5 descase 10 segundos",
            2: "4x10",
            3: "3x até a falha",
            4: "Puxada alta",
            5: "2s em baixo 3x15",
            6: "4x10",
            7: "4x10",
            8: "3x12"
        },
        "exercicios_posteriorombro":{
            1: "Peck deck invertido com drop",
            2: "Remada alta Smith",
            3: "Encolhimento trapezio",
            4: "Posterior de ombro no cabo médio",
            5: "Posterior de ombro no banco 45º"
        },
        "repeticoes_posteriorombro": {
            1: "3x15/15",
            2: "3x12",
            3: "4x10",
            4: "4x12",
            5: "1x12 2x20 a cada 5 descanse 10 segundos" 
        },
        "exercicios_posteriorcoxa":{
            1: "Mesa flexora",
            2: "Cadeira flexora",
            3: "stiff",
            4: "Elevação pélvica(pode ser no smith)"
        },
        "repeticoes_posteriorcoxa": {
            1:"4x10",
            2: "3x12",
            3: "3x12",
            4: "3x8 (pesado)"
        }
    },
    "treino_b": {
        "exercicios_quadriceps": {
            1: "Agachamento Livre",
            2: "Leg Press",
            3: "Cadeira extensora",
            4: "Passada",
            5: "Bulgaro com Halter",
            6: "Afundo com Halter"
        },
        "repeticoes_quadriceps": {
            1: "4x10",
            2: "4x12",
            3: "1x20 e 3x12",
            4: "5 min",
            5: "4x10",
            6: "4x15",
            
        },
        "exercicios_panturrilha":{
            1: "Gêmeos em pé"
        },
        "repeticoes_panturrilha": {
            1: "5x12 2s alongando e 2s contraindo"
        },
        "exercicios_adutor": {
            1:"Cadeira Adutora"
        },
        "repeticoes_adutor": {
            1:"1x12 3x20 a cada 5 descase 10s"
        }
    },
    "treino_c": { 
 
        "exercicios_peito": {
            1: "Supino inclinado com halteres ou articulado",
            2: "Supino reto com barra",
            3: "Voador",
            4: "Flexão 60 rep",
            5: "Cross-over declinado",
            6: "Supino inclinado no Cross"
            
            
        },
        "repeticoes_peito": {
            1: "4x12",
            2: "1x15 3x8",
            3: "4x10",
            4: "6x10",
            5: "4x10",
            6:"5x10 2s no pico de contração",
            
        },
        "exercicios_panturrilha": {
            1:"Panturrilha no smith com degrau"
        },
        "repeticoes_panturrilha": {
            1: "5x10 15s de descanso"
        }
    },
    "treino_d": {
        "exercicios_biceps": {
            1: "Rosca Direta",
            2: "Rosca Scott Unilatral",
            3: "Biceps na polia alta unilateral",
            4: "Biceps no banco 45º martelo simultaneo",
            5: "Rosca alternada"
        },
        "repeticoes_biceps": {
            1: "4x10",
            2: "4x10 (controlado)",
            3: "3x15",
            4: "4x10",
            5: "3x12 4s descendo 2s contraindo"
        },
        "exercicios_triceps": {
            1: "Triceps com barra na polia",
            2: "Triceps com corda polia",
            3: "Triceps na polia unilateral",
            4: "Triceps testa com barra W",
            5: "Triceps no supino (pegada fechada)"
        },
        "repeticoes_triceps": {
            1: "4x8 (pesado)",
            2: "4x12",
            3: "3x15",
            4: "3x8",
            5: "4x10"
        }
    },
    "treino_e": {
        "exercicios_ombro": {
            1: "Desenvolvimento com halteres + Elevação frontal com barra",
            2: "Elevação lateral com halter drop set",
            3: "Elevação lateral na polia",
            4: "Desenvolvimento arnold"
        },
        "repeticoes_ombro": {
            1: "3x15 + 15",
            2: "3x6-8-10 3x10-8-6",
            3: "4x10",
            4: "3x12"
        },
        "exercicios_panturrilha": {
            1: "Panturrilha unilateral degrau"
        },

        "repeticoes_panturrilha": {
            1: "3x20 a cada 10 descase 10 segundos"
        }
    }
}


    #basal = float(basal) + 300
    # Parte 2: Plano de Treino
    prompt_treino = f"""
Baseando-se nos exercícios e repetições a seguir:

Treino A:
- Exercícios de costas: {dados_exemplo['treino_a']['exercicios_costas']}
- Repetições de costas: {dados_exemplo['treino_a']['repeticoes_costas']}
- Exercícios de posterior de ombro: {dados_exemplo['treino_a']['exercicios_posteriorombro']}
- Repetições de posterior de ombro: {dados_exemplo['treino_a']['repeticoes_posteriorombro']}
- Exercícios de posterior de coxa: {dados_exemplo['treino_a']['exercicios_posteriorcoxa']}
- Repetições de posterior de coxa: {dados_exemplo['treino_a']['repeticoes_posteriorcoxa']}

Treino B:
- Exercícios de quadríceps: {dados_exemplo['treino_b']['exercicios_quadriceps']}
- Repetições de quadríceps: {dados_exemplo['treino_b']['repeticoes_quadriceps']}
- Exercício de panturrilha: {dados_exemplo['treino_b']['exercicios_panturrilha']}
- Repetição de panturrilha: {dados_exemplo['treino_b']['repeticoes_panturrilha']}
- Exercício de adutor: {dados_exemplo['treino_b']['exercicios_adutor']}
- Repetição de adutor: {dados_exemplo['treino_b']['repeticoes_adutor']}

Treino C:
- Exercícios de peito: {dados_exemplo['treino_c']['exercicios_peito']}
- Repetições de peito: {dados_exemplo['treino_c']['repeticoes_peito']}
- Exercício de panturrilha: {dados_exemplo['treino_c']['exercicios_panturrilha']}
- Repetição de panturrilha: {dados_exemplo['treino_c']['repeticoes_panturrilha']}

Treino D:
- Exercícios de bíceps: {dados_exemplo['treino_d']['exercicios_biceps']}
- Repetições de bíceps: {dados_exemplo['treino_d']['repeticoes_biceps']}
- Exercícios de tríceps: {dados_exemplo['treino_d']['exercicios_triceps']}
- Repetições de tríceps: {dados_exemplo['treino_d']['repeticoes_triceps']}

Treino E:
- Exercícios de ombro: {dados_exemplo['treino_e']['exercicios_ombro']}
- Repetições de ombro: {dados_exemplo['treino_e']['repeticoes_ombro']}
- Exercício de panturrilha: {dados_exemplo['treino_e']['exercicios_panturrilha']}
- Repetição de panturrilha: {dados_exemplo['treino_e']['repeticoes_panturrilha']}

Agora, crie um plano de treino detalhado para A, B, C, D, E conforme as regras:
1. No treino A, escolha 4 exercícios de costas, 2 de posterior de ombro e 2 de posterior de coxa.
2. No treino B, escolha 4 exercícios de quadríceps, 1 de panturrilha e 1 de adutor.
3. No treino C, escolha 4 exercícios de peito e 1 de panturrilha.
4. No treino D, escolha 3 de bíceps e 3 de tríceps, intercalando-os.
5. No treino E, escolha 3 de ombro (incluindo obrigatoriamente "Elevação lateral com halter drop set") e 1 de panturrilha.

Inclua o nome dos exercícios e as repetições de forma detalhada.
"""


    # Parte 3: Plano de Dieta
    if alimento:
        restricao_alimentos = f"Evite incluir os seguintes alimentos na dieta: {alimento}."
    else:
        restricao_alimentos = ""

    prompt_dieta = f"""
    Elabore um plano de dieta para {nome} que tem o basal de 2000kcal com o objetivo de {objetivo}, dividido em 5 refeições: café da manhã, almoço, lanche da tarde, jantar e ceia.
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
        response_treino = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_treino}],
            max_tokens=1000,
            temperature=0.7
        )
        
        response_dieta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_dieta}],
            max_tokens=1000,
            temperature=0.7
        )
        
        # Combina as partes
        # tmb_text = response_tmb.choices[0].message["content"]
        treino_text = response_treino.choices[0].message["content"]
        dieta_text = response_dieta.choices[0].message["content"]
        
        # Texto final
        return f"1. Taxa Metabólica Basal (TMB):\n 2000 \n\n2. Ficha de Treino:\n{treino_text}\n\n3. Plano de Dieta:\n{dieta_text}"

    except Exception as e:
        print(f"Erro ao acessar OpenAI: {e}")
        return "Não foi possível gerar o plano de treino e dieta no momento."


def gerar_pdf(nome_arquivo, nome_usuario, plano_treino_dieta):
    try:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Página 1: TMB e Plano de Treino
        pdf.add_page()
        pdf.set_font("Arial", style="B", size=16)
        pdf.cell(200, 10, txt=f"Plano de Treino e Dieta de {nome_usuario}", ln=True, align="C")
        pdf.ln(10)

        # Conteúdo da TMB e Treino
        pdf.set_font("Arial", size=12)
        treino_conteudo = plano_treino_dieta.split("\n\n3. Plano de Dieta:")[0]  # Parte do treino
        pdf.multi_cell(0, 10, txt=treino_conteudo)

        # Página 2: Plano de Dieta
        pdf.add_page()
        pdf.set_font("Arial", style="B", size=16)
        pdf.cell(200, 10, txt="Plano de Dieta e Observações", ln=True, align="C")
        pdf.ln(10)

        # Conteúdo do Plano de Dieta
        dieta_conteudo = plano_treino_dieta.split("\n\n3. Plano de Dieta:")[1]  # Parte da dieta
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=dieta_conteudo)

        # Salva o PDF
        pdf.output(nome_arquivo)
        print(f"PDF gerado com sucesso: {nome_arquivo}")
        return True
    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        return False



