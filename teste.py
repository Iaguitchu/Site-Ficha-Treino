from PyPDF2 import PdfReader, PdfWriter, PageObject
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

# Função para adicionar texto ao PDF
def adicionar_texto_pdf(input_pdf, output_pdf, dados):
    # Ler o PDF original
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for page_number, page in enumerate(reader.pages):
        # Criar um buffer para a nova camada
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Helvetica-Bold", 12)
        can.setFillColorRGB(255, 255, 255)

        # Adicionar texto dependendo da página
        if page_number == 0:  # Página 1, por exemplo
            can.drawString(20, 535, f"{dados.get('treino_a', '')}")
            can.drawString(100, 680, f"Treino B: {dados.get('treino_b', '')}")
        elif page_number == 1:  # Página 2, por exemplo
            can.drawString(100, 700, f"Café da Manhã: {dados.get('cafe_manha', '')}")
            can.drawString(100, 680, f"Almoço: {dados.get('almoco', '')}")

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
    "treino_a": "Supino Reto - 3x12",
    "treino_b": "Rosca Direta - 3x15",
    "cafe_manha": "Ovos e aveia",
    "almoco": "Frango com batata doce",
}

# Chamar a função com o PDF enviado
adicionar_texto_pdf("C:\Projetos\Site Academia/Ficha de treino academia.pdf", "Ficha_treino_editado.pdf", dados_exemplo)
