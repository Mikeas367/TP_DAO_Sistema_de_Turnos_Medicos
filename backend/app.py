from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 

from routes.medicoRouter import router as medicoRouter
from routes.especialidadRouter import router as especialidadRouter
from routes.turnoRouter import router as turnoRouter
from routes.pacientesRouter import router as pacienteRouter   # <-- agregado
from routes.reportesRouter import router as reportesRouter
from routes.recetaRouter import router as recetaRouter
from routes.agendaRouter import router as agendaRouter
from routes.historiaClinicaRouter import router as historialRouter

app = FastAPI(title="Sistema de Turnos Médicos")

# ========== RUTAS ==========
app.include_router(medicoRouter, prefix="/api", tags=["medicos"])
app.include_router(especialidadRouter, prefix="/api")
app.include_router(turnoRouter, prefix="/api")
app.include_router(pacienteRouter, prefix="/api")              # <-- agregado aquí
app.include_router(reportesRouter, prefix="/api")
app.include_router(recetaRouter, prefix="/api")
app.include_router(agendaRouter, prefix="/api")
app.include_router(historialRouter, prefix="/api")

# ========== CORS ==========
origins = [
    "http://localhost:5173",  # Frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== RUTA PRINCIPAL ==========
@app.get("/")
def root():
    return {"message": "API Sistema de Turnos Médicos funcionando 🚑"}
