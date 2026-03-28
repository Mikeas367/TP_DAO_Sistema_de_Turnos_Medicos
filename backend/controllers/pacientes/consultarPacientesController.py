from interfaces.interfacePersistencia import IRepository
from interfaces.interfacePersistencia import IRepository
from fastapi import HTTPException, status

class ConsultarPacientesController:
    def __init__(self, paciente_repo: IRepository):
        self.paciente_repo = paciente_repo

    def obtener_pacientes(self):
        try:
            pacientes = self.paciente_repo.getAll()
            return pacientes
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontraron Pacientes"
            )

    def obtener_paciente_por_id(self, id: int):
        return self.paciente_repo.getById(id)