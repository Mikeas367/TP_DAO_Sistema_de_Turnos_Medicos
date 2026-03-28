from pydantic import BaseModel
from datetime import date

class RecetaCreate(BaseModel):
    paciente_id: int
    medico_id: int
    fecha_emision: date
    detalle_medicamento: str
    tratamiento: str

class RecetaResponse(RecetaCreate):
    receta_id: int

    class Config:
        orm_mode = True
