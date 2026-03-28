from datetime import datetime
from typing import Optional
from models.paciente import Paciente
from models.medico import Medico
from models.estado import Estado

class Turno:
    def __init__(self, id: Optional[int], paciente: Optional[Paciente], medico: Medico, estado: Estado, fecha):
        self.id = id
        self.paciente = paciente
        self.medico = medico
        self.estado = estado
        self.fecha = fecha

    def marcar_asistencia(self, estado: Estado):
        self.estado = estado
    
    def marcar_inasistencia(self, estado: Estado):
        self.estado = estado

    def esta_libre(self):
        return self.estado.es_libre()
    
    def esta_ocupado(self):
        return self.estado.es_ocupado()
    
    def solicitar_turno(self, estado: Estado, paciente: Paciente):
        if self.esta_libre:
            self.estado = estado
            self.paciente = paciente
            print("SE OCUPO EL TURNO")

    def liberar_turno(self, estado: Estado):
        self.estado = estado
        self.paciente = None
    
    def es_asistido(self):
        return self.estado.es_asistido()
    
    def es_no_asistido(self):
        return self.estado.es_no_asistido()


    def __str__(self):
        return f"Turno ID: {self.id}, Estado: {self.estado.nombre}"
    
    def sos_de_medico(self, medico_id: int):
        print(f"parametro: {medico_id} El que tiene el Turno: {self.medico.id}")
        return self.medico.id == medico_id

    def estas_entre_fechas(self, fecha_desde, fecha_hasta):
        fecha_desde = datetime.strptime(fecha_desde, "%Y-%m-%d").date()
        fecha_hasta = datetime.strptime(fecha_hasta, "%Y-%m-%d").date()
        fecha_turno = datetime.strptime(self.fecha, "%Y-%m-%d %H:%M:%S")

        if fecha_desde <= fecha_turno.date() <= fecha_hasta:
            return True
        else:
            return False
        