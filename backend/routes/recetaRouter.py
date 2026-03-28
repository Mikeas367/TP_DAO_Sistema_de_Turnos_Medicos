from fastapi import APIRouter
from schemas.recetaSchema import RecetaCreate, RecetaResponse
from controllers.receta.recetaController import recetacontroller
from database import Database
from fastapi.responses import FileResponse
import os

router = APIRouter(prefix="/recetas", tags=["Recetas"])

db = Database()

@router.post("/", response_model=RecetaResponse)
def crear_receta_endpoint(receta: RecetaCreate):
    return recetacontroller.crear_receta_controller(db, receta)

@router.get("/", response_model=list[RecetaResponse])
def listar_recetas_endpoint():
    return recetacontroller.listar_recetas_controller(db)

@router.get("/{receta_id}/pdf")
def descargar_pdf(receta_id: int):
    ruta = f"pdfs/receta_{receta_id}.pdf"

    if not os.path.exists(ruta):
        return {"error": "El PDF no existe"}

    return FileResponse(
        ruta,
        media_type="application/pdf",
        filename=f"receta_{receta_id}.pdf"
    )
