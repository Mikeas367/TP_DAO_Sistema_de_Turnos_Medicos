from fastapi import APIRouter, HTTPException
from schemas.pacienteSchema import PacienteBase, PacienteUpdate
from database import Database
from repositories.sqlitePacienteRepository import SqlitePacienteRepository
from controllers.pacientes.pacientesController import PacienteController

router = APIRouter() 

db = Database()
paciente_repo = SqlitePacienteRepository(db)
paciente_controller = PacienteController(paciente_repo)

@router.post("/pacientes")
def alta_paciente(paciente: PacienteBase):
    print("Entro al POST---------> " + paciente.email)
    paciente_controller.crear_paciente(
        nombre=paciente.nombre,
        apellido=paciente.apellido,
        email=paciente.email
    )
    return {"mensaje": "Paciente creado"}

@router.get("/pacientes")
def listar_pacientes():
    pacientes = paciente_controller.listar_pacientes()
    return pacientes

@router.get("/pacientes/{id}")
def obtener_paciente(id: int):
    paciente_controller.obtener_paciente(id)

@router.put("/pacientes/{id}")
def actualizar_paciente(id: int, paciente: PacienteUpdate):
    paciente_controller.actualizar_paciente(
        id=id,
        nombre=paciente.nombre,
        apellido=paciente.apellido,
        email=paciente.email
    )

@router.delete("/pacientes/{id}")
def eliminar_paciente(id: int):
    paciente_controller.eliminar_paciente_por_id(id)
