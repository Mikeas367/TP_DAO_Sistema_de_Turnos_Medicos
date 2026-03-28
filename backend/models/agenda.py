from typing import List, Optional
from datetime import date, datetime, timedelta
from models.diaLaboral import DiaLaboral
from models.turno import Turno
from models.estado import Estado

# dia_semana: int | 0: lunes; 1: martes; 2: miercoles; 3: jueves; 4: viernes; 5: sabado
class Agenda:
    def __init__(self, id: Optional[int], medico, dias_trabajo: List[DiaLaboral]):
        self.id = id
        self.medico = medico
        self.dias_trabajo = dias_trabajo   # LISTA DE DIAS

    def generar_turnos(self, fecha_desde: date, fecha_hasta: date, estado: Estado):
        turnos_creados = []
        fecha_actual = fecha_desde
        delta = timedelta(days=1)

        while fecha_actual <= fecha_hasta:

            # Filtrar reglas del día
            reglas = [d for d in self.dias_trabajo if d.dia_semana == fecha_actual.weekday()]

            for regla in reglas:

                hora = datetime.combine(fecha_actual, regla.hora_inicio)
                hora_fin = datetime.combine(fecha_actual, regla.hora_fin)

                while hora <= hora_fin:
                    turno = Turno(
                        id=None,
                        paciente=None,
                        medico=self.medico,
                        estado=estado,
                        fecha=hora
                    )
                    turnos_creados.append(turno)

                    hora += timedelta(minutes=regla.duracion_turno_min)

            fecha_actual += delta

        return turnos_creados

    