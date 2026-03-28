from interfaces.interfacePersistencia import IRepository
from schemas.turnoSchema import TurnoConsulta
from models.turno import Turno
from fastapi import HTTPException, status
from datetime import datetime

class RegistraInAsistenciaController:
    def __init__(self, turno_repo: IRepository, estados_repo: IRepository):
        self.turno_repo = turno_repo
        self.estados_repo = estados_repo


    def registrarInAsistencia(self, turno: TurnoConsulta):
        turno_a_marcar = self.buscar_turno(turno.turno_id)
        estado_no_asistido = self.buscar_estado_no_asistido()
        fecha_turno_str = turno_a_marcar.fecha

        print("FECHA RECIBIDA:", fecha_turno_str)
        fecha_turno = datetime.strptime(fecha_turno_str, "%Y-%m-%d %H:%M:%S")
        fechaHoraActual = datetime.now()

        if fecha_turno > fechaHoraActual:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se puede cancelar el turno ya que todavia no es la fecha"
            )
        else:
            turno_a_marcar.marcar_inasistencia(estado_no_asistido)
            self.turno_repo.update(turno_a_marcar)



    def buscar_estado_no_asistido(self):
        estados = self.estados_repo.getAll()
        for estado in estados:
            if estado.es_no_asistido():
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