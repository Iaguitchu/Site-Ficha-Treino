import random

from PyPDF2 import PdfReader, PdfWriter, PageObject
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import textwrap

# def listar_exercicios_e_repeticoes():

dados_exemplo = {
    "treino_a": {
        "exercicios_costas": {
            1: "Remada Curvada Pronada a cada 5 descanse 10 segundos",
            2: "Remada Curvada Supinada",
            3: "Barra Fixa",
            4: "Puxada alta contraia 2s e volta em 4s",
            5: "Pulldown com corda segure 2s em baixo",
            6: "Remada sentado",
            7: "Remada Unilateral (serrote)",
            8: "Remada com Halteres Banco 45º",
        },
        "repeticoes_costas": {
            1: "1x12 2x20 ",
            2: "4x10",
            3: "3x até a falha",
            4: "3x10, 1x15",
            5: "3x15",
            6: "4x10",
            7: "4x10",
            8: "3x12"
        },
        "exercicios_posteriorombro":{
            1: "Peck deck invertido com drop",
            2: "Remada alta Smith",
            3: "Posterior de ombro no cabo médio",
            4: "Posterior de ombro no banco 45º a cada 5 descanse 10 segundos"
        },
        "repeticoes_posteriorombro": {
            1: "3x15/15",
            2: "3x12",
            3: "4x12",
            4: "1x12 2x20 " 
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
    "treino_c": {
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
            1: "Gêmeos em pé 2s alongando e 2s contraindo"
        },
        "repeticoes_panturrilha": {
            1: "5x12 "
        },
        "exercicios_adutor": {
            1:"Cadeira Adutora a cada 5 descanse 10s"
        },
        "repeticoes_adutor": {
            1:"1x12 3x20"
        }
    },
    "treino_b": { 
 
        "exercicios_peito": {
            1: "Supino inclinado com halteres ou articulado",
            2: "Supino reto com barra",
            3: "Voador",
            4: "Flexão 60 rep",
            5: "Cross-over declinado",
            6: "Supino inclinado no Cross 2 segundos no pico de contração"
            
            
        },
        "repeticoes_peito": {
            1: "4x12",
            2: "1x15 3x8",
            3: "4x10",
            4: "6x10",
            5: "4x10",
            6:"5x10 ",
            
        },
        "exercicios_biceps": {
            1: "Rosca Simultanea com halteres",
            2: "Rosca Concentrada",
            3: "Rosca Alternada banco 45º"            
            
        },
        "repeticoes_biceps": {
            1: "4x12",
            2: "1x15 3x8",
            3: "4x10"
            
        },
        "exercicios_panturrilha": {
            1:"Panturrilha no smith com degrau 15segundos de descanso"
        },
        "repeticoes_panturrilha": {
            1: "5x10"
        }
    },
    "treino_d": {
        "exercicios_biceps": {
            1: "Rosca Direta",
            2: "Rosca Scott Unilatral",
            3: "Biceps na polia alta unilateral",
            4: "Biceps no banco 45º martelo simultaneo",
            5: "Rosca alternada 4s descendo 2s contraindo"
        },
        "repeticoes_biceps": {
            1: "4x10",
            2: "4x10 (controlado)",
            3: "3x15",
            4: "4x10",
            5: "3x12"
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
            4: "Desenvolvimento arnold",
            5: "Elevação lateral no banco 45º",
            6: "Elevação frontal pegada supinada no banco 45º",
            7: "Encolhimento trapezio"
        },
        "repeticoes_ombro": {
            1: "3x15 + 15",
            2: "3x6-8-10 3x10-8-6",
            3: "4x10",
            4: "3x12",
            5: "4x10",
            6: "3x15",
            7: "4x10",
        },
        "exercicios_panturrilha": {
            1: "Panturrilha unilateral degrau descanse 10 segundos"
        },

        "repeticoes_panturrilha": {
            1: "3x20"
        }
    }
}
    

def gerar_treino_aleatorio(dados_exemplo):
    plano_treino = {}
    
    # Regras específicas de cada treino
    regras_treino = {
        "treino_a": {
            "exercicios_costas": 4,
            "exercicios_posteriorombro": 2,
            "exercicios_posteriorcoxa": 2,
        },
        "treino_b": {
            "exercicios_peito": 4,
            "exercicios_panturrilha": 1,
            "exercicios_biceps": 2
        },
        "treino_c": {
            "exercicios_quadriceps": 4,
            "exercicios_panturrilha": 1,
            "exercicios_adutor": 1,
        },
        "treino_d": {
            "exercicios_biceps": 3,
            "exercicios_triceps": 3,
        },
        "treino_e": {
            "exercicios_ombro": 4,
            "exercicios_panturrilha": 1,
        }
    }
    
    # Iterar pelos treinos e selecionar os exercícios
    for treino, grupos in regras_treino.items():
        plano_treino[treino] = {}  # Inicializa o treino
        for grupo, qtd in grupos.items():
            # Verificar se o grupo existe nos dados
            if grupo in dados_exemplo[treino]:
                # Selecionar aleatoriamente os exercícios do grupo
                exercicios = random.sample(list(dados_exemplo[treino][grupo].items()), qtd)
                
                # Adicionar os exercícios e suas repetições ao plano
                plano_treino[treino][grupo] = {
                    nome: dados_exemplo[treino][f"repeticoes_{grupo.split('_')[1]}"].get(idx, "Repetição não encontrada")
                    for idx, nome in exercicios
                }
            else:
                plano_treino[treino][grupo] = "Grupo não encontrado"
    
    return plano_treino


# Função para adicionar texto ao PDF
def adicionar_texto_pdf(input_pdf, output_pdf, dados, dados2):
    # Ler o PDF original
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for page_number, page in enumerate(reader.pages):
        # Criar um buffer para a nova camada
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Helvetica-Bold", 10)
        can.setFillColorRGB(255, 255, 255)  # Cor do texto (preto)

        # Adicionar texto dependendo da página
        if page_number == 0:  # Página 1
            y_position_text= 665  # Posição inicial no eixo Y
            y_position_text2 = 650
            y_position_rep = 650

            # Iterar pelos grupos de exercícios do treino A
            for grupo, exercicios in dados["treino_a"].items():
                if isinstance(exercicios, dict):  # Certificar que é um grupo válido
                    for nome, repeticao in exercicios.items():
                        # Quebrar texto em múltiplas linhas se ultrapassar 35 caracteres
                        linhas = textwrap.wrap(nome, width=30)
                        print(linhas, len(linhas))
                        for index, linha in enumerate(linhas):  # Use enumerate para obter o índice e o valor
                            if len(linhas) > 1:
                                if index == 0:  # Se for o índice 0
                                    can.drawString(20, y_position_text, linha)  # Nome do exercício na posição text
                                elif index == 1:  # Se for o índice 1
                                    print(f"Segunda linha: {linha}")
                                    can.drawString(20, y_position_text2, linha)  # Nome do exercício na posição text2
                                else:
                                    # Caso tenha mais linhas, ajuste a posição dinamicamente
                                    y_position_text2 -= 10
                                    print(f"Linha adicional: {linha}")
                                    can.drawString(20, y_position_text2, linha)
                            else:
                                can.drawString(20, y_position_text2, linha)
                                

                        can.drawString(200, y_position_rep, f"{repeticao}")  # Repetições

                        y_position_text -= 35
                        y_position_text2 -= 35
                        y_position_rep -= 35

            # Repetir para treino B
            y_position_text = 665
            y_position_text2 = 650
            y_position_rep = 650

            for grupo, exercicios in dados["treino_b"].items():
                if isinstance(exercicios, dict):  # Certificar que é um grupo válido
                    for nome, repeticao in exercicios.items():
                        # Quebrar texto em múltiplas linhas se ultrapassar 35 caracteres
                        linhas = textwrap.wrap(nome, width=30)
                        for index, linha in enumerate(linhas):  # Use enumerate para obter o índice e o valor
                            if len(linhas) > 1:
                                if index == 0:  # Se for o índice 0
                                    can.drawString(300, y_position_text, linha)  # Nome do exercício na posição text
                                elif index == 1:  # Se for o índice 1
                                    print(f"Segunda linha: {linha}")
                                    can.drawString(300, y_position_text2, linha)  # Nome do exercício na posição text2
                                else:
                                    # Caso tenha mais linhas, ajuste a posição dinamicamente
                                    y_position_text2 -= 10
                                    print(f"Linha adicional: {linha}")
                                    can.drawString(300, y_position_text2, linha)
                            else:
                                can.drawString(300, y_position_text2, linha)
                                

                        can.drawString(480, y_position_rep, f"{repeticao}")  # Repetições
                        y_position_text -= 35
                        y_position_text2 -= 35
                        y_position_rep -= 35

            # Repetir para treino C
            y_position_text = 300
            y_position_text2 = 285
            y_position_rep = 285
            
            for grupo, exercicios in dados["treino_c"].items():
                if isinstance(exercicios, dict):  # Certificar que é um grupo válido
                    for nome, repeticao in exercicios.items():
                        # Quebrar texto em múltiplas linhas se ultrapassar 35 caracteres
                        linhas = textwrap.wrap(nome, width=30)
                        print(linhas, len(linhas))
                        for index, linha in enumerate(linhas):  # Use enumerate para obter o índice e o valor
                            if len(linhas) > 1:
                                if index == 0:  # Se for o índice 0
                                    can.drawString(20, y_position_text, linha)  # Nome do exercício na posição text
                                elif index == 1:  # Se for o índice 1
                                    print(f"Segunda linha: {linha}")
                                    can.drawString(20, y_position_text2, linha)  # Nome do exercício na posição text2
                                else:
                                    # Caso tenha mais linhas, ajuste a posição dinamicamente
                                    y_position_text2 -= 10
                                    print(f"Linha adicional: {linha}")
                                    can.drawString(20, y_position_text2, linha)
                            else:
                                can.drawString(20, y_position_text2, linha)
                                

                        can.drawString(200, y_position_rep, f"{repeticao}")  # Repetições
                        y_position_text -= 35
                        y_position_text2 -= 35
                        y_position_rep -= 35

             # Repetir para treino C
            y_position_text = 300
            y_position_text2 = 285
            y_position_rep = 285
            
            for grupo, exercicios in dados["treino_d"].items():
                if isinstance(exercicios, dict):  # Certificar que é um grupo válido
                    for nome, repeticao in exercicios.items():
                        # Quebrar texto em múltiplas linhas se ultrapassar 35 caracteres
                        linhas = textwrap.wrap(nome, width=30)
                        for index, linha in enumerate(linhas):  # Use enumerate para obter o índice e o valor
                            if len(linhas) > 1:
                                if index == 0:  # Se for o índice 0
                                    can.drawString(300, y_position_text, linha)  # Nome do exercício na posição text
                                elif index == 1:  # Se for o índice 1
                                    print(f"Segunda linha: {linha}")
                                    can.drawString(300, y_position_text2, linha)  # Nome do exercício na posição text2
                                else:
                                    # Caso tenha mais linhas, ajuste a posição dinamicamente
                                    y_position_text2 -= 10
                                    print(f"Linha adicional: {linha}")
                                    can.drawString(300, y_position_text2, linha)
                            else:
                                can.drawString(300, y_position_text2, linha)
                                

                        can.drawString(480, y_position_rep, f"{repeticao}")  # Repetições
                        y_position_text -= 35
                        y_position_text2 -= 35
                        y_position_rep -= 35



        elif page_number == 1:  # Página 2
            y_position_text = 600
            y_position_text2 = 585
            y_position_rep = 585

            for grupo, exercicios in dados["treino_e"].items():
                if isinstance(exercicios, dict):  # Certificar que é um grupo válido
                    for nome, repeticao in exercicios.items():
                        # Quebrar texto em múltiplas linhas se ultrapassar 35 caracteres
                        linhas = textwrap.wrap(nome, width=30)
                        for index, linha in enumerate(linhas):  # Use enumerate para obter o índice e o valor
                            if len(linhas) > 1:
                                if index == 0:  # Se for o índice 0
                                    can.drawString(165, y_position_text, linha)  # Nome do exercício na posição text
                                elif index == 1:  # Se for o índice 1
                                    print(f"Segunda linha: {linha}")
                                    print(y_position_text2)
                                    can.drawString(165, y_position_text2, linha)  # Nome do exercício na posição text2
                                else:
                                    # Caso tenha mais linhas, ajuste a posição dinamicamente
                                    y_position_text2 -= 10
                                    print(f"Linha adicional: {linha}")
                                    can.drawString(165, y_position_text2, linha)
                            else:
                                 can.drawString(165, y_position_text2, linha)
                                

                        can.drawString(350, y_position_rep, f"{repeticao}")  # Repetições
                        y_position_text -= 35
                        y_position_text2 -= 35
                        y_position_rep -= 35


        elif page_number == 2:  # Página 3 - Dieta
            y_position = 580
            x_position = 40

            for refeicao, itens in dados2["dieta"].items():
                for item in itens:
                    can.drawString(x_position, y_position, f"- {item}")
                    y_position -= 20  # Ajusta a posição vertical para o próximo item
                    if y_position < 80:
                        y_position = 580
                        x_position += 200

        can.showPage()  # Finaliza a página atual no canvas
        can.save()  # Salva o buffer

        # Combinar com a página original
        packet.seek(0)
        overlay = PdfReader(packet)
        overlay_page = overlay.pages[0]

        # Adicionar a sobreposição à página original
        page.merge_page(overlay_page)
        writer.add_page(page)

    # Salvar o PDF resultante
    with open(output_pdf, "wb") as output:
        writer.write(output)



dados_exemplo2 = {
    "dieta": {
        "cafe_manha": {
            "30g whey, 3 bananas"
        },
        "almoço":{
            "100g arroz, 130g frango"
        },
        "cafe_tarde":{
            "2 ovos, 2 pão panco"
        },
        "janta":{
            "100g arroz, 130g frango"
        },
        "ceia":{
            "hipercalorico"
    }
    }
    }


plano = gerar_treino_aleatorio(dados_exemplo)


# Chamar a função com o PDF enviado
adicionar_texto_pdf("C:\Projetos\Site-Ficha-Treino/Ficha de treino academia.pdf", "Ficha_treino_editado.pdf", plano, dados_exemplo2)
