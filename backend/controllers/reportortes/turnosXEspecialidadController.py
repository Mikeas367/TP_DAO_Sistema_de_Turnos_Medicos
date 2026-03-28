import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

from interfaces.interfacePersistencia import IRepository

class ReporteTurnosXEspecialidad:

    def __init__(self, turno_repo: IRepository, especialidad_repo: IRepository):
        self.turno_repo = turno_repo
        self.especialidad_repo = especialidad_repo


    def buscar_turnos_entre_fechas(self, fecha_desde, fecha_hasta):
        turnos_entre_fechas = []
        turnos = self.turno_repo.getAll()

        for turno in turnos:
            if turno.estas_entre_fechas(fecha_desde, fecha_hasta):
                turnos_entre_fechas.append(turno)
        
        return turnos_entre_fechas
    

    # ===============================
    # 🔹 Contar turnos por especialidad
    # ===============================
    def conteo_por_especialidades(self, especialidades, turnos):
        contador = {}
        #contador = {esp.nombre: 0 for esp in especialidades}
        for especialiad in especialidades:
            contador[especialiad.nombre] = 0
            
        for turno in turnos:
            esp_nombre = turno.medico.especialidad.nombre
            contador[esp_nombre] += 1
            print(contador)

        return contador
    

    # ===============================
    # 🔹 Reporte principal con filtro fechas
    # ===============================
    def generarReporte(self, desde, hasta):

        especialidades = self.especialidad_repo.getAll()
        turnos = self.buscar_turnos_entre_fechas(desde, hasta)

        contador = self.conteo_por_especialidades(especialidades, turnos)

        return self.generar_grafico_barras(contador, desde, hasta)


    # ===============================
    # 🔹 Generación del PDF
    # ===============================
    def generar_grafico_barras(self, data_conteo, desde, hasta):

        filename = f"Reports/reporte_turnos_especialidad_{desde}_a_{hasta}.pdf"
        carpeta = os.path.dirname(filename)

        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta)

        # ------------------------------------------
        # 1. Generar el gráfico de barras
        # ------------------------------------------
        especialidades = list(data_conteo.keys())
        cantidades = list(data_conteo.values())

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(especialidades, cantidades, color="#1F77B4")

        ax.set_xlabel("Especialidad", fontsize=12)
        ax.set_ylabel("Cantidad de Turnos", fontsize=12)
        ax.set_title("Turnos por Especialidad", fontsize=16, fontweight="bold")
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        plt.xticks(rotation=45, ha="right")

        for bar in bars:
            y = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, y + 0.1, int(y),
                    ha="center", va="bottom", fontsize=11)

        grafico_path = "Reports/grafico_especialidades.png"
        plt.tight_layout()
        plt.savefig(grafico_path, dpi=150)
        plt.close()

        # ------------------------------------------
        # 2. Crear el PDF con ReportLab
        # ------------------------------------------
        doc = SimpleDocTemplate(filename, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        titulo = ParagraphStyle(
            "titulo",
            parent=styles["Title"],
            fontSize=22,
            alignment=1,
            textColor=colors.HexColor("#1F4E79"),
            spaceAfter=20,
        )


        story.append(Paragraph("Reporte de Turnos por Especialidad", titulo))
        story.append(Paragraph(f"Período: <b>{desde}</b> a <b>{hasta}</b>", styles["Heading3"]))
        story.append(Spacer(1, 20))


        story.append(Image(grafico_path, width=420, height=300))
        story.append(Spacer(1, 20))


        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        story.append(Paragraph(f"Generado el {fecha_actual}", styles["Normal"]))

        doc.build(story)

        os.remove(grafico_path)

        return filename
