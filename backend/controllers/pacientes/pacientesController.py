from models.paciente import Paciente
from interfaces.interfacePersistencia import IRepository

class PacienteController:
    def __init__(self, repository: IRepository):
        self.repository = repository

    def crear_paciente(self, nombre: str, apellido: str, email: str):
        paciente = Paciente(None, nombre, apellido, email)
        print("Se crea El pacienteee", paciente)
        self.repository.save(paciente)
        return paciente

    def listar_pacientes(self):
        pacientes = self.repository.getAll()
        return pacientes
    
    def obtener_paciente(self, id: int):
        pacientes = self.repository.getAll()
        for paciente in pacientes:
            if paciente["id"] == id:
                return paciente
        return None
    
    def eliminar_paciente_por_id(self, id: int) -> bool:
        try:
            self.repository.deleteById(id)
        except Exception:
            return False
        
    def actualizar_paciente(self, id: int, nombre: str, apellido: str, email: str) -> bool:
        paciente_existente = self.repository.getById(id)
        if not paciente_existente:
            return False
        self.repository.update(id, nombre, apellido, email)
        return True