from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime

class ReportePacientesAtendidos:
    def __init__(self, turno_repo):
        self.turno_repo = turno_repo

    def generarReportePacientesAtendidos(self, desde: str, hasta: str):
        try:
            turnos = self.turno_repo.getPacientesAtendidos(desde, hasta)

            # Se arma un JSON legible
            return [
                {
                    "paciente_id": t["paciente_id"],
                    "nombre": t["nombre"],
                    "apellido": t["apellido"],
                    "email": t["email"],       
                    "fecha": t["fecha"]        
                }
                for t in turnos
            ]

        except Exception as e:
            return {"error": str(e)}

    def generar_pdf(self, desde: str, hasta: str):
        # Obtener los pacientes atendidos desde el repositorio
        turnos = self.turno_repo.getPacientesAtendidos(desde, hasta)

        # Convertir filas SQL a diccionarios si vienen como tuplas
        pacientes = [
            {"nombre": t[1], "apellido": t[2], "fecha": t[3]} if isinstance(t, tuple) else t
            for t in turnos
        ]

        # Crear un buffer para el PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        title = Paragraph("📋 Pacientes Atendidos", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 12))

        # Tabla de datos
        data = [["Nombre", "Apellido", "Fecha"]]
        for p in pacientes:
            data.append([p["nombre"], p["apellido"], p["fecha"]])

        table = Table(data, hAlign='LEFT', colWidths=[150, 150, 120])
        table.setStyle(
            TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 12),
                ('BOTTOMPADDING', (0,0), (-1,0), 8),
                ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ])
        )

        elements.append(table)
        doc.build(elements)

        buffer.seek(0)
        return buffer