from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

def generar_receta_pdf(receta):
    ruta_carpeta = "pdfs"
    os.makedirs(ruta_carpeta, exist_ok=True)

    archivo = os.path.join(ruta_carpeta, f"receta_{receta['receta_id']}.pdf")

    doc = SimpleDocTemplate(archivo)
    styles = getSampleStyleSheet()
    story = []

    # ⚠️ Convertir fecha a string sí o sí
    fecha = receta["fecha_emision"]
    if not isinstance(fecha, str):
        fecha = str(fecha)

    story.append(Paragraph(f"<b>RECETA MÉDICA</b>", styles["Title"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"ID Receta: {receta['receta_id']}", styles["Normal"]))
    story.append(Paragraph(f"Médico: Dr. {receta['medico_nombre']} {receta['medico_apellido']}", styles["Normal"]))
    story.append(Paragraph(f"Paciente: {receta['paciente_nombre']} {receta['paciente_apellido']}", styles["Normal"]))
    story.append(Paragraph(f"Fecha de emisión: {fecha}", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Detalle del medicamento:</b>", styles["Heading3"]))
    story.append(Paragraph(receta["detalle_medicamento"], styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Tratamiento:</b>", styles["Heading3"]))
    story.append(Paragraph(receta["tratamiento"], styles["Normal"]))

    doc.build(story)

    return archivo
