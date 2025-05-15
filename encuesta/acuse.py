
from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch, cm
from reportlab.pdfgen import canvas
import os
from io import BytesIO

def generate_document(output_filename=None, variables=None, return_bytes=False):
    """
    Genera un documento PDF usando canvas directamente en lugar de SimpleDocTemplate.
    
    Args:
        output_filename: Nombre del archivo donde guardar el PDF (opcional)
        variables: Diccionario con variables para el documento
        return_bytes: Si es True, retorna los bytes del PDF en lugar de guardarlo
    
    Returns:
        BytesIO object si return_bytes es True, None en otro caso
    """
    if variables is None:
        variables = {}
    
    # Crear buffer o archivo de salida
    if return_bytes:
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=LETTER)
    else:
        p = canvas.Canvas(output_filename, pagesize=LETTER)
    
    page_w, page_h = LETTER
    
    # --- Marca de agua con opacidad fija ---
    wm = variables.get('watermark_path', '')
    if os.path.exists(wm):
        # Ajustar opacidad
        p.saveState()
        p.setFillAlpha(0.2)
        
        wm_w, wm_h = 6 * inch, 6 * inch
        x = (page_w - wm_w) / 2
        y = (page_h - wm_h) / 2
        p.drawImage(wm, x, y, width=wm_w, height=wm_h, mask='auto')
        
        p.restoreState()
    else:
        p.saveState()
        p.setFont("Helvetica-Bold", 60)
        p.setFillColor(colors.lightgrey)
        p.drawCentredString(page_w/2, page_h/2, "ESTADOS UNIDOS MEXICANOS")
        p.restoreState()

    # --- Encabezado superior: SEP logo + texto TECNM a la derecha ---
    sep_logo = variables.get('logo_sep_path', '')
    logo_w, logo_h = 1.5*inch, 0.6*inch
    margin = 72  # 1 pulgada en puntos
    y_logo = page_h - margin - logo_h + 20

    if os.path.exists(sep_logo):
        p.drawImage(sep_logo, margin, y_logo,
                   width=logo_w, height=logo_h, preserveAspectRatio=True)

    p.setFont("Helvetica-Bold", 9)
    p.setFillColor(colors.black)
    p.drawRightString(page_w - margin, y_logo + logo_h - 2, "TECNOLÓGICO NACIONAL DE MÉXICO")
    p.drawRightString(page_w - margin, y_logo + logo_h - 14, "INSTITUTO TECNOLÓGICO DE VERACRUZ")

    # --- Contenido principal ---
    # Spacer para empujar el bloque principal hacia abajo
    y_current = page_h - margin - 1.5 * inch
    
    # DEPENDENCIA (alineada a la derecha)
    p.setFont("Helvetica-Bold", 11)
    dep_text = f"DEPENDENCIA: {variables.get('dependencia', '')}"
    p.drawRightString(page_w - margin, y_current, dep_text)
    
    # EXPEDIENTE (debajo, misma alineación)
    y_current -= 14
    exp_text = f"EXPEDIENTE: {variables.get('expediente', '')}"
    p.drawRightString(page_w - margin, y_current, exp_text)
    
    # Separación
    y_current -= 5 * cm
    
    # A QUIEN CORRESPONDA (centrado horizontalmente)
    p.setFont("Helvetica-Bold", 11)
    p.drawCentredString(page_w - 6.5*margin, y_current, "A QUIEN CORRESPONDA:")

    # Separación
    y_current -= 1 * cm
    p.setFont("Helvetica", 11)
    p.drawCentredString(page_w - 5.8*margin, y_current, "Por medio de la presente hago constar que el C.")
    
    y_current -= 1 * cm

    nombre_text = f"{variables.get('nombre', '')}"
    p.setFont("Helvetica", 11)
    p.drawString(page_w/2, y_current, nombre_text)

    y_current -= 1 * cm
    # Contenido principal
    p.setFont("Helvetica", 11)
    content = variables.get('content', '')
    
    # Implementación básica de texto con saltos de línea
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_JUSTIFY
    
    # Crear un estilo para el párrafo
    style = ParagraphStyle(
        'Normal',
        fontName='Helvetica',
        fontSize=11,
        alignment=TA_JUSTIFY,
        textColor=colors.black
    )
    
    # Crear el párrafo y obtener su altura
    para = Paragraph(content, style)
    w, h = para.wrap(page_w - 2*margin, 500)  # Limitar el ancho
    
    # Dibujar el párrafo
    para.drawOn(p, margin, y_current - h)
    
    # Actualizar la posición vertical
    y_current -= (h + 2 * cm)
    
    # CADENA DIGITAL
    cadena_text = f"CADENA DIGITAL: {variables.get('cadena_digital', '')}"
    p.setFont("Helvetica-Bold", 11)
    p.drawString(margin, y_current, "CADENA DIGITAL:")
    
    y_current -= 12
    p.setFont("Helvetica", 11)
    p.drawString(margin, y_current, variables.get('cadena_digital', ''))
    
    # Separación
    y_current -= 2 * cm
    
    # Firma
    p.drawString(margin, y_current, variables.get('signature', ''))

    # --- Pie de página: logo ITV + dirección centrada ---
    footer = variables.get('logo_footer_path', '')
    logo_size = 0.8*inch
    y_footer = margin - 0.5*cm

    if os.path.exists(footer):
        p.drawImage(footer, margin, y_footer,
                   width=logo_size, height=logo_size, preserveAspectRatio=True)
    
    p.setFont("Helvetica", 6)
    
    p.drawRightString(page_w/2 + 30, y_footer + logo_size/2 - 3, 
                    "Calz. Miguel Ángel de Quevedo 2779, Col. Formando Hogar. C.P. 91897")
    p.drawRightString(page_w/2 - 55, y_footer + logo_size/2 - 10, 
                    "H. Veracruz, Ver.")
    p.drawRightString(page_w/2 - 50, y_footer + logo_size/2 - 17, 
                    "Tel. (229) 934 15 00")
    p.drawRightString(page_w/2 - 30, y_footer + logo_size/2 - 24, 
                    "https://www.veracruz.tecnm.mx")

    # Finalizar la página y guardar el documento
    p.showPage()
    p.save()

    
    # Si se solicitó retornar los bytes
    if return_bytes:
        buffer.seek(0)
        return buffer
    return None


# === Ejemplo de uso ===
if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    IMAGES_DIR = "templates/static/img" 
    vars = {
        'nombre': 'pichule',
        'dependencia': 'Encuesta de Satisfacción Egresados',
        'expediente': '12345678',
        'content': (
            "Perteneciente a la carrera de <b>Ingeniería Química</b> realizó la encuesta de satisfacción "
            "de egresados en la modalidad <b>en línea</b> el día <b>10 de mayo de 2025</b> "
            "en la hora marcada como <b>14:30</b> correspondiente al periodo <b>Enero-Junio 2025</b>. "
            "Por tal motivo sus registros correspondientes a sus datos personales han quedado registrados satisfactoriamente."
        ),
        'cadena_digital': 'ABCDEF123456789',
        'signature': 'Nombre y firma autorizada',
        'direccion': (
            "Calz. Miguel Ángel de Quevedo 2779, Col. Formando Hogar. C.P. 91897 H. Veracruz, Ver. Tel. (229) 934 15 00 · https://www.veracruz.tecnm.mx"
        ),
        'logo_sep_path': os.path.join(IMAGES_DIR, 'sepB.png'),
        'logo_footer_path': os.path.join(IMAGES_DIR, 'logo.png'),
        'watermark_path': os.path.join(IMAGES_DIR, 'uemex.jpg')
    }

    # Verificar existencia de imágenes
    for key in ['logo_sep_path', 'logo_footer_path', 'watermark_path']:
        if not os.path.exists(vars[key]):
            print(f"Advertencia: no se encontró {vars[key]}")

    # Ejemplo de uso para guardar en un archivo
    generate_document("acuse.pdf", vars)
    
    # Ejemplo de uso para obtener bytes
    # pdf_bytes = generate_document(return_bytes=True, variables=vars)
    # Ahora puedes hacer algo con pdf_bytes, como enviarlo como respuesta HTTP