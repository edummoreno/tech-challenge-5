# Importar bibliotecas
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Registrar fontes Unicode para evitar "caixas pretas" em caracteres especiais
pdfmetrics.registerFont(TTFont("DejaVuSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))


# Função para gerar o relatório STRIDE em pdf
def gerar_relatorio_pdf(lista_jsons, output_pdf_path):

    # Carregar estilos base do ReportLab para customização
    styles = getSampleStyleSheet()

    # Definir estilos de texto para chave/valor e formatação monoespaçada
    base = ParagraphStyle(
        "Base",
        parent=styles["Normal"],
        fontName="DejaVuSans",
        fontSize=11,
        leading=14,
        alignment=TA_LEFT,
    )
    key = ParagraphStyle(
        "Key",
        parent=base,
        fontName="DejaVuSans-Bold",
        spaceBefore=8,
    )
    mono = ParagraphStyle(
        "Mono",
        parent=base,
        fontName="DejaVuSans",
        fontSize=10.5,
        leading=13,
    )

    # Configurar o documento PDF (A4 e margens)
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=2.2 * cm,
        rightMargin=2.2 * cm,
        topMargin=2.0 * cm,
        bottomMargin=2.0 * cm,
    )

    def esc(s):
        # Para não quebrar o Paragraph com caracteres especiais
        if s is None:
            return ""
        s = str(s)
        return (
            s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
        )
    
    # Lista de elementos para serem renderizados no PDF.
    story = []

    for idx, item in enumerate(lista_jsons):
        data = json.loads(item) if isinstance(item, str) else item

        class_name = data.get("class_name", "")
        components = data.get("components", []) or []
        stride_analysis = data.get("stride_analysis", []) or []

        # class_name:
        story.append(Paragraph("class_name:", key))
        story.append(Paragraph(f"&nbsp;&nbsp;{esc(class_name)}", mono))
        story.append(Spacer(1, 6))

        # components:
        story.append(Paragraph("components:", key))
        if components:
            for c in components:
                story.append(Paragraph(f"&nbsp;&nbsp;- {esc(c)}", mono))
        else:
            story.append(Paragraph("&nbsp;&nbsp;- (vazio)", mono))
        story.append(Spacer(1, 8))

        # stride_analysis:
        story.append(Paragraph("stride_analysis:", key))

        if not stride_analysis:
            story.append(Paragraph("&nbsp;&nbsp;- (vazio)", mono))
        else:
            for block in stride_analysis:
                t = block.get("type", "")
                threat = block.get("threat", "")
                cms = block.get("countermeasures", []) or []

                story.append(Paragraph(f"&nbsp;&nbsp;- type: {esc(t)}", mono))
                story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;threat: {esc(threat)}", mono))
                story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;countermeasures:", mono))

                if cms:
                    for cm_txt in cms:
                        story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- {esc(cm_txt)}", mono))
                else:
                    story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- (vazio)", mono))

                story.append(Spacer(1, 6))

        # Quebra de página entre classes
        if idx < len(lista_jsons) - 1:
            story.append(PageBreak())

    doc.build(story)
    print("====================================")
    print("Relatório STRIDE gerado com sucesso.")
    print("====================================\n")
