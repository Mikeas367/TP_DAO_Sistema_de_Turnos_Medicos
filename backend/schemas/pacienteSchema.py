from pydantic import BaseModel, Field, EmailStr

class PacienteBase(BaseModel):
    nombre: str = Field(..., min_length=2)
    apellido: str = Field(..., min_length=2)
    email: EmailStr

class PacienteUpdate(BaseModel):
    nombre: str = Field(..., min_length=2)
    apellido: str = Field(..., min_length=2)
    email: EmailStr