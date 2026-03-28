from sqlalchemy import Column, Integer, String, Date
from database import Base

class Receta(Base):
    __tablename__ = "recetas"
    receta_id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, nullable=False)
    medico_id = Column(Integer, nullable=False)
    fecha_emision = Column(Date, nullable=False)
    detalle_medicamento = Column(String, nullable=False)
    tratamiento = Column(String, nullable=False)
