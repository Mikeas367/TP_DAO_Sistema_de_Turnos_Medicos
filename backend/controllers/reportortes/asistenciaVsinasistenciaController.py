import os
from datetime import datetime

# ========= FIX PARA EVITAR ERROR DE TKINTER ==========
import matplotlib
matplotlib.use("Agg")   # Backend sin GUI
# =====================================================

import matplotlib.pyplot as plt

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4


class ReporteAsistencia:

    def __init__(self, turno_repo):
        self.turno_repo = turno_repo

    def generarReporteAsistencia(self, desde: str, hasta: str):

        datos = self.turno_repo.obtener_asistencias_inasistencias(desde, hasta)

        asistencias = datos[0] if datos and datos[0] is not None else 0
        inasistencias = datos[1] if datos and datos[1] is not None else 0

        # ============================
        #  1) GENERACIÓN DEL GRÁFICO
        # ============================

        labels = ["Asistencias", "Inasistencias"]

        # Sanitizar valores
        asistencias = asistencias if isinstance(asistencias, (int, float)) and asistencias >= 0 else 0
        inasistencias = inasistencias if isinstance(inasistencias, (int, float)) and inasistencias >= 0 else 0

        sizes = [asistencias, inasistencias]

        # Si ambos son cero, evitar NaN
        if sum(sizes) == 0:
            # Crear gráfico "vacío" de forma segura
            plt.figure(figsize=(5,5))
            plt.text(0.5, 0.5, "Sin datos para mostrar", ha="center", va="center", fontsize=14)
        else:
            plt.figure(figsize=(5, 5))
            plt.pie(
                sizes,
                labels=labels,
                autopct='%1.1f%%',
                wedgeprops={"linewidth": 1, "edgecolor": "white"},
                textprops={'fontsize': 12}
            )

        plt.title("Asistencias vs Inasistencias", fontsize=16)
        grafico_path = "Reports/grafico_asistencia.png"
        plt.savefig(grafico_path, dpi=150, bbox_inches="tight")
        plt.close()


        # ============================
        #  2) GENERACIÓN DEL PDF
        # ============================
        fechaHoraActual = datetime.now()
        nombre_pdf = f"reporte_asistencias_{desde}_a_{hasta}.pdf"
        ruta_pdf = f"Reports/{nombre_pdf}"

        doc = SimpleDocTemplate(ruta_pdf, pagesize=A4, rightMargin=40, leftMargin=40)
        styles = getSampleStyleSheet()
        story = []

        # Título general
        titulo_estilo = ParagraphStyle(
            'titulo',
            parent=styles['Title'],
            fontSize=22,
            alignment=1,
            spaceAfter=20,
            textColor=colors.HexColor("#1F4E79")
        )

        story.append(Paragraph("Reporte de Asistencias", titulo_estilo))
        story.append(Paragraph(f"Período: <b>{desde}</b> a <b>{hasta}</b>", styles["Heading3"]))
        story.append(Spacer(1, 20))

        # Resumen en tabla
        data_resumen = [
            ["Tipo", "Cantidad"],
            ["Asistencias", asistencias],
            ["Inasistencias", inasistencias],
        ]

        tabla_resumen = Table(data_resumen, colWidths=[200, 150])
        tabla_resumen.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1F4E79")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("BACKGROUND", (0,1), (-1,-1), colors.HexColor("#E8F0FE")),
            ("GRID", (0,0), (-1,-1), 1, colors.black),
            ("FONTSIZE", (0,0), (-1,-1), 12),
        ]))

        story.append(tabla_resumen)
        story.append(Spacer(1, 30))

        # Sección del gráfico
        story.append(Paragraph("Gráfico de Asistencias", styles["Heading2"]))
        story.append(Spacer(1, 10))
        story.append(Image(grafico_path, width=350, height=350))
        story.append(Spacer(1, 30))

        # Footer
        story.append(Paragraph(
            f"Reporte generado automáticamente el {fechaHoraActual.strftime('%d/%m/%Y - %H:%M')}",
            styles["Normal"]
        ))

        doc.build(story)

        # Borrar archivo temporal del gráfico
        if os.path.exists(grafico_path):
            os.remove(grafico_path)

        return ruta_pdf
