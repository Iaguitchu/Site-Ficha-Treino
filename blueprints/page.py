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
    sexo = dados.get("sexo")
    
    print(f"Nome: {nome}, Email: {email}, Alimento: {alimento}")

    # Salva no banco de dados
    sqlExecute("""insert into cliente ( objetivo, nome, email, idade, altura, peso, data_cadastro) 
                  values (%s,%s,%s,%s,%s,%s,NOW())""", (objetivo, nome, email, idade, altura, peso))
    
    basal = calcular_basal(sexo, peso, altura, idade)
    
    # Gera o plano de treino e dieta
    plano = gerar_plano_treino_dieta(nome, idade, objetivo, alimento, basal)

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


def gerar_plano_treino_dieta(nome, idade, objetivo, alimento, basal):
    dados_exemplo = {
    "treino_a": {
        "exercicios": {
            1: "Remada Curvada Pronada",
            2: "Remada Curvada Supinada",
            3: "Barra Fixa",
            4: "Puxada alta",
            5: "Pulldown com corda segure",
            6: "Remada sentado",
            7: "Remada Unilateral (serrote)",
            8: "Peck deck invertido com drop",
            9: "Remada com Halteres Banco 45º",
            10: "Mesa flexora",
            11: "Cadeira flexora",
            12: "stiff",
            13: "Elevação pélvica(pode ser no smith)"
        },
        "repeticoes": {
            1: "4x12",
            2: "4x10",
            3: "3x até a falha",
            4: "Puxada alta",
            5: "2s em baixo 3x15",
            6: "4x10",
            7: "4x10",
            8: "3x15/15",
            9: "3x12",
            10: "4x10",
            11: "3x12",
            12: "3x12",
            13: "3x8 (pesado)"
        }
    },
    "treino_b": {
        "exercicios": {
            1: "Agachamento Livre",
            2: "Leg Press",
            3: "Cadeira extensora",
            4:"passada",
            5:"bulgaro",
            6: "afundo",
            7: "Gêmeos em pé"
        },
        "repeticoes": {
            1: "4x10",
            2: "4x12",
            3: "1x20 e 3x12",
            4: "5 min",
            5: "4x10",
            6: "4x15",
            7: "5x12 2s alongando e 2s contraindo"
        }
    },
    "treino_c": { 
 
        "exercicios": {
            1: "Supino inclinado com halteres ou articulado",
            2: "Supino reto com barra",
            3: "Voador",
            4: "Flexão 60 rep",
            5: "Cross-over declinado",
            6: "Supino inclinado no Cross",
            7:"Panturrilha no smith com degrau"
            
        },
        "repeticoes": {
            1: "4x12",
            2: "1x15 3x8",
            3: "4x10",
            4: "6x10",
            5: "4x10",
            6:"5x10 2s no pico de contração",
            7: "5x10 15s de descanso"
        }
    },
    "treino_d": {
        "exercicios": {
            1: "Supino Reto",
            2: "Crucifixo Inclinado",
            3: "Flexão de Braço"
        },
        "repeticoes": {
            1: "3x12",
            2: "4x10",
            3: "3x15"
        }
    },
    "treino_e": {
        "exercicios": {
            1: "Supino Reto",
            2: "Crucifixo Inclinado",
            3: "Flexão de Braço"
        },
        "repeticoes": {
            1: "3x12",
            2: "4x10",
            3: "3x15"
        }
    }
}

    # Parte 1: Calcular TMB
    prompt_tmb = f"esse é o basal {basal}, de {nome}"

    basal = float(basal) + 300
    # Parte 2: Plano de Treino
    prompt_treino = f"""
    Crie um plano de treino de hipertrofia focado em {objetivo} para {nome}, com base no Basal de {basal} + 300 kcal. O treino deve ser dividido precisa ser dividido desse jeito que vou passar
    e me de um resultado em um dicionario python desse jeito:
    
    
    Escolha 4 exercicios para costas dessa lista que passei, e 3 para posteriors:
    - Segunda-feira: Costas:
        (Remada Curvada Pronada 4x12, Remada Curvada Supinada 4x10, Barra Fixa 3x até a falha, Puxada alta segure 2s em baixo 3x12, Pulldown com corda segure 2s em baixo 3x15, remada sentado 4x10, Remada Unilateral (serrote) 4x10
    
    Posterior de ombro:
        Peck deck invertido com drop 3x15/15
    
    Posterior de cocha:
        (Mesa flexora 4x10, cadeira flexora 3x12, stiff, elevação pélvica(pode ser no smith) 3x12)
    
    
    
    Escolha 4 exercicio de peito e coloque o exercicio de panturrilha no começo do treino
    - Terça-feira: Peito
        (supino inclinado com halteres ou articulado 4x12, supino reto com barra 1x15 3x8, voador 4x10, flexão 60 rep 6x10, cross-over declinado 4x10)
    
    Panturrilha:
        (panturrilha no smith com degrau 5x10 15s de descanso)
    
    
    
    - Quarta-feira: Descanso
    
    
    
    Escolha 4 exercicio de quadríceps e coloque pra fazer panturrilha no final do treino
    - Quinta-feira: Pernas
        (agachamento livre ou smith com pés alinhados com tronco 4x10, leg-press 4x12, cadeira extensora 1x20 3x12, 5 min passada, bulgaro 4x10, afundo 4x15)
    
    Panturrilha:
        Gêmeos em pé 5x12 (pesado, 2s alongando)

    
    
    Pode passar esses exatos exercicios nessa ordem
    - Sexta-feira: Braços
        (Rosca Direta 4x10, Triceps com corda polia 4x12, Rosca Scott Unilatral 4x10, Triceps com barra na polia 4x10, Biceps na polia alta unilateral 3x15, Triceps na polia unilateral 3x15, Biceps no banco 45 martelo simultaneo 4x10, triceps testa com barra W 3x8)
    

    - Sábado: Ombros
        (Desenvolvimento com halteres + Elevação frontal com barra 3x15, Elevação lateral com halter drop set 3x10-8-6, Elevação lateral na polia 4x10, Encolhimento com Barra 4x12 ) 
    
    
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
        tmb_text = response_tmb.choices[0].message["content"]
        treino_text = response_treino.choices[0].message["content"]
        dieta_text = response_dieta.choices[0].message["content"]
        
        # Texto final
        return f"1. Taxa Metabólica Basal (TMB):\n{tmb_text}\n\n2. Ficha de Treino:\n{treino_text}\n\n3. Plano de Dieta:\n{dieta_text}"

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



