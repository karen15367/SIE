from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.units import inch, cm
from reportlab.pdfgen import canvas as pdfcanvas
import os


def generate_document(output_filename, variables):
    # Crear documento
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=LETTER,
        rightMargin=72, leftMargin=72,
        topMargin=72, bottomMargin=72
    )

    # Definir estilos con color negro
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        'Justify',
        alignment=TA_JUSTIFY,
        fontSize=11,
        spaceAfter=12,
        textColor=colors.black
    ))
    styles.add(ParagraphStyle(
        'CenterBold',
        alignment=TA_CENTER,
        fontSize=11,
        spaceAfter=12,
        fontName='Helvetica-Bold',
        textColor=colors.black
    ))
    styles.add(ParagraphStyle(
        'RightBold',
        alignment=TA_RIGHT,
        fontSize=11,
        spaceAfter=6,
        fontName='Helvetica-Bold',
        textColor=colors.black
    ))

    content = []

    # Spacer para empujar el bloque principal hacia abajo
    content.append(Spacer(1, 1.5 * inch))

    # DEPENDENCIA (alineada a la derecha)
    content.append(Paragraph(
        f"<b>DEPENDENCIA:</b> {variables['dependencia']}", styles['RightBold']))
    # EXPEDIENTE (debajo, misma alineación)
    content.append(Paragraph(
        f"<b>EXPEDIENTE:</b> {variables['expediente']}", styles['RightBold']))
    content.append(Spacer(1, 0.5 * cm))

    # A QUIEN CORRESPONDA (centrado horizontalmente)
    content.append(Paragraph("A QUIEN CORRESPONDA:", styles['CenterBold']))
    content.append(Spacer(1, 0.3 * cm))

    # Contenido principal
    content.append(Paragraph(variables['content'], styles['Justify']))
    content.append(Spacer(1, 0.5 * cm))

    # CADENA DIGITAL
    content.append(Paragraph(
        f"<b>CADENA DIGITAL:</b><br/>{variables['cadena_digital']}", styles['Justify']))
    content.append(Spacer(1, 1 * cm))

    # Firma
    content.append(Paragraph(variables['signature'], styles['Justify']))

    # Generar PDF
    doc.build(
        content,
        onFirstPage=lambda canv, d: add_page_elements(canv, d, variables),
        onLaterPages=lambda canv, d: add_page_elements(canv, d, variables)
    )


def add_page_elements(canvas, doc, variables):
    canvas.saveState()
    page_w, page_h = LETTER

    # --- Marca de agua con opacidad fija ---
    wm = variables.get('watermark_path', '')
    if os.path.exists(wm):
        # Ajustar opacidad (ReportLab ≥3.5)
        try:
            canvas.setFillAlpha(0.2)
        except AttributeError:
            pass

        wm_w, wm_h = 6 * inch, 6 * inch
        x = (page_w - wm_w) / 2
        y = (page_h - wm_h) / 2
        canvas.drawImage(wm, x, y, width=wm_w, height=wm_h, mask='auto')

        try:
            canvas.setFillAlpha(1)
        except AttributeError:
            pass
    else:
        canvas.setFont("Helvetica-Bold", 60)
        canvas.setFillColor(colors.lightgrey)
        canvas.drawCentredString(
            page_w/2, page_h/2, "ESTADOS UNIDOS MEXICANOS")
        canvas.setFillColor(colors.black)

    # --- Encabezado superior: SEP logo + texto TECNM a la derecha ---
    sep_logo = variables.get('logo_sep_path', '')
    logo_w, logo_h = 1.5*inch, 0.6*inch
    y_logo = page_h - doc.topMargin - logo_h + 20

    if os.path.exists(sep_logo):
        canvas.drawImage(sep_logo, doc.leftMargin, y_logo,
                         width=logo_w, height=logo_h, preserveAspectRatio=True)

    canvas.setFont("Helvetica-Bold", 9)
    canvas.setFillColor(colors.black)
    canvas.drawRightString(page_w - doc.rightMargin,
                           y_logo + logo_h - 2, "TECNOLÓGICO NACIONAL DE MÉXICO")
    canvas.drawRightString(page_w - doc.rightMargin, y_logo +
                           logo_h - 14, "INSTITUTO TECNOLÓGICO DE VERACRUZ")

    # --- Pie de página: logo ITV + dirección centrada ---
    footer = variables.get('logo_footer_path', '')
    logo_size = 0.8*inch
    y_footer = doc.bottomMargin - 0.5*cm

    if os.path.exists(footer):
        canvas.drawImage(footer, doc.leftMargin, y_footer,
                        width=logo_size, height=logo_size, preserveAspectRatio=True)
    canvas.setFont("Helvetica", 6)
    canvas.setFillColor(colors.black)
    '''
    canvas.drawCentredString(page_w/2, y_footer +
                            logo_size/2 - 3, variables['direccion'])
    '''
    
    canvas.drawRightString(page_w/2 + 30, y_footer +
                        logo_size/2 - 3, "Calz. Miguel Ángel de Quevedo 2779, Col. Formando Hogar. C.P. 91897")
    canvas.drawRightString(page_w/2 - 55, y_footer +
                        logo_size/2 - 10, "H. Veracruz, Ver.")
    canvas.drawRightString(page_w/2 - 50, y_footer +
                        logo_size/2 - 17, "Tel. (229) 934 15 00")
    canvas.drawRightString(page_w/2 - 30, y_footer +
                        logo_size/2 - 24, "https://www.veracruz.tecnm.mx")

    canvas.restoreState()


# === Ejemplo de uso ===
if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    vars = {
        'dependencia': 'ANEXO Quím y bio Quím.',
        'expediente': '12345678',
        'content': (
            "Perteneciente a la carrera de <b>{carrera}</b> realizó el anexo "
            "perteneciente a la carrera de Quím y Bio Quím el día <b>{fecha}</b> "
            "en la hora marcada como <b>{hora}</b> correspondiente al periodo <b>{periodo}</b>. "
            "Por tal motivo sus registros correspondientes a sus datos personales han quedado registrados satisfactoriamente."
        ),
        'cadena_digital': 'ABCDEF123456789',
        'signature': 'Nombre y firma autorizada',
        'direccion': (
            "Calz. Miguel Ángel de Quevedo 2779, Col. Formando Hogar. C.P. 91897 H. Veracruz, Ver. Tel. (229) 934 15 00 · https://www.veracruz.tecnm.mx"
        ),
        'logo_sep_path': os.path.join(here, 'sepB.png'),
        'logo_footer_path': os.path.join(here, 'logo.png'),
        'watermark_path': os.path.join(here, 'uemex.jpg')
    }

    # Verificar existencia de imágenes
    for key in ['logo_sep_path', 'logo_footer_path', 'watermark_path']:
        if not os.path.exists(vars[key]):
            print(f"Advertencia: no se encontró {vars[key]}")

    generate_document("acuse.pdf", vars)
