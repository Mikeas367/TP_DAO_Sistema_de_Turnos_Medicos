from fastapi import APIRouter, Query
from fastapi.responses import FileResponse, StreamingResponse

from database import Database
from repositories.sqliteTurnoRepository import SqliteTurnoRepository
from repositories.sqliteEspecialidadRepository import SqliteEspecialidadRepository

from controllers.reportortes.asistenciaVsinasistenciaController import ReporteAsistencia
from controllers.reportortes.turnosXEspecialidadController import ReporteTurnosXEspecialidad
from controllers.reportortes.pacientesAtendidosController import ReportePacientesAtendidos


router = APIRouter()

db = Database()
turno_repo = SqliteTurnoRepository(db)
especialidad_repo = SqliteEspecialidadRepository(db)

# Instancias correctas
reporte_asistencia = ReporteAsistencia(turno_repo=turno_repo)
reporte_turno_especialidad = ReporteTurnosXEspecialidad(
    turno_repo=turno_repo, 
    especialidad_repo=especialidad_repo
)
reporte_pacientes_atendidos = ReportePacientesAtendidos(turno_repo=turno_repo)



@router.get("/asistencia-vs-inasistencias")
def obtener_reporte_asistencia(desde: str, hasta: str):
    return reporte_asistencia.generarReporteAsistencia(desde, hasta)


@router.get("/asistencia-vs-inasistencias-pdf")
def obtener_reporte_asistencia_pdf(desde: str, hasta: str):
    ruta_pdf = reporte_asistencia.generarReporteAsistencia(desde, hasta)
    return FileResponse(
        ruta_pdf,
        media_type="application/pdf",
        filename=f"reporte_asistencia_{desde}_a_{hasta}.pdf"
    )


# ---------------------------
#   TURNOS POR ESPECIALIDAD
# ---------------------------

@router.get("/turno_x_especialidad")
def generar_reporte_turno_x_especialidad(desde: str, hasta: str):
    return reporte_turno_especialidad.generarReporte(desde, hasta)


@router.get("/turno_x_especialidad_pdf")
def descargar_pdf_turnos_especialidad(desde: str, hasta: str):
    ruta_pdf = reporte_turno_especialidad.generarReporte(desde, hasta)
    return FileResponse(
        ruta_pdf,
        media_type="application/pdf",
        filename=f"turnos_especialidad_{desde}_a_{hasta}.pdf"
    )


# ---------------------------
#   PACIENTES ATENDIDOS
# ---------------------------

@router.get("/pacientes-atendidos")
def pacientes_atendidos(desde: str = Query(...), hasta: str = Query(...)):
    return reporte_pacientes_atendidos.generarReportePacientesAtendidos(desde, hasta)


@router.get("/pacientes-atendidos-pdf")
def descargar_pdf_pacientes(desde: str = Query(...), hasta: str = Query(...)):
    pdf_buffer = reporte_pacientes_atendidos.generar_pdf(desde, hasta)
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=pacientes_{desde}_a_{hasta}.pdf"
        }
    )
