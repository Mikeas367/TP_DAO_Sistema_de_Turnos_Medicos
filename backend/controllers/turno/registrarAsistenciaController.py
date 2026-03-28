from interfaces.interfacePersistencia import IRepository
from schemas.turnoSchema import TurnoConsulta, TurnoAsistencia
from models.turno import Turno
from models.historiaClinica import HistoriaClinica
from fastapi import HTTPException, status
from datetime import datetime

class RegistraAsistenciaController:
    def __init__(self, turno_repo: IRepository, estados_repo: IRepository, historia_clinica_repo: IRepository):
        self.turno_repo = turno_repo
        self.estados_repo = estados_repo
        self.historia_clinica_repo = historia_clinica_repo
        self.fecha_hora_actual = None

    def obtener_fecha_hora_actual(self):
        fechaHoraActual = datetime.now()
        fecha_parseada = fechaHoraActual.strftime("%Y-%m-%d")
        self.fecha_hora_actual = fecha_parseada
    
    def registrarAsistencia(self, turno: TurnoAsistencia):
        turno_a_marcar = self.buscar_turno(turno.turno_id)
        
        estado_asistido = self.buscar_estado_asistido()
        self.obtener_fecha_hora_actual()

        medico = turno_a_marcar.medico  
        paciente = turno_a_marcar.paciente
    


        turno_a_marcar.marcar_asistencia(estado_asistido)
        historia_nueva = HistoriaClinica(None, medico, self.fecha_hora_actual, paciente, turno.detalle_diagnostico, turno.tratamiento)
        self.historia_clinica_repo.save(historia_nueva)
        self.turno_repo.update(turno_a_marcar)



    def buscar_estado_asistido(self):
        estados = self.estados_repo.getAll()
        for estado in estados:
            if estado.es_asistido():
                return estado
    
    def buscar_turno(self, turno_id: int)-> Turno:
        p =  self.turno_repo.getById(turno_id)
        if not p:
            #error HTTP para el front
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró el turno con id {turno_id}"
            )
        return p