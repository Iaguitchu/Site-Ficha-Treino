from PyPDF2 import PdfReader, PdfWriter, PageObject
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

# Função para adicionar texto ao PDF
# Função para adicionar texto ao PDF
def adicionar_texto_pdf(input_pdf, output_pdf, dados, dados2):
    # Ler o PDF original
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for page_number, page in enumerate(reader.pages):
        # Criar um buffer para a nova camada
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Helvetica-Bold", 12)
        can.setFillColorRGB(255, 255, 255)  # Cor do texto (preto)

        # Adicionar texto dependendo da página
        if page_number == 0:  # Página 1
            y_position = 560  # Posição inicial no eixo Y
            


            for index, exercicio in dados["treino_a"]["exercicios"].items():
                print(y_position, "A")
                repeticao = dados["treino_a"]["repeticoes"][index]
                can.drawString(20, y_position, f" {exercicio}")
                can.drawString(210, y_position, f" {repeticao}")
                y_position -= 25  # Ajusta a posição vertical para o próximo item
    
            y_position = 560

            for index, exercicio in dados["treino_b"]["exercicios"].items():
                print(y_position, "B")
                repeticao = dados["treino_b"]["repeticoes"][index]
                can.drawString(305, y_position, f" {exercicio}")
                can.drawString(500, y_position, f" {repeticao}")
                y_position -= 25
                
            y_position = 255

            for index, exercicio in dados["treino_b"]["exercicios"].items():
                print(y_position, "C")
                repeticao = dados["treino_c"]["repeticoes"][index]
                can.drawString(20, y_position, f" {exercicio}")
                can.drawString(210, y_position, f" {repeticao}")
                y_position -= 25

            y_position = 255

            for index, exercicio in dados["treino_b"]["exercicios"].items():
                print(y_position, "D")
                repeticao = dados["treino_c"]["repeticoes"][index]
                can.drawString(305, y_position, f" {exercicio}")
                can.drawString(500, y_position, f" {repeticao}")
                y_position -= 25

        elif page_number == 1:  # Página 2
            y_position = 520  # Posição inicial no eixo Y
            


            for index, exercicio in dados["treino_a"]["exercicios"].items():
                print(y_position, "A")
                repeticao = dados["treino_a"]["repeticoes"][index]
                can.drawString(160, y_position, f" {exercicio}")
                can.drawString(360, y_position, f" {repeticao}")
                y_position -= 25  # Ajusta a posição vertical para o próximo item
            
            
            
        elif page_number == 2:  # Página 3 - Dieta
            y_position = 580
            x_position = 40

            for refeicao, itens in dados2["dieta"].items():
                for item in itens:
                    can.drawString(x_position, y_position, f"- {item}")
                    y_position -= 220  # Ajusta a posição vertical para o próximo item
                    if y_position == -80:
                        y_position = 580
                        x_position = 340


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

# Dados de exemplo para preenchimento
dados_exemplo = {
    "treino_a": {
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
    "treino_b": {
        "exercicios": {
            1: "Agachamento Livre",
            2: "Leg Press",
            3: "Stiff"
        },
        "repeticoes": {
            1: "4x10",
            2: "4x12",
            3: "3x12"
        }
    },
    "treino_c": {
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

# Chamar a função com o PDF enviado
adicionar_texto_pdf("C:\Projetos\Site Academia/Ficha de treino academia.pdf", "Ficha_treino_editado.pdf", dados_exemplo, dados_exemplo2)
