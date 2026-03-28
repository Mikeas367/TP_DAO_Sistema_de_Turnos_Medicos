from fastapi import APIRouter
from database import Database
from repositories.sqliteHistoriaClinicaRepository import SqliteHistoriaClinicaRepository


router = APIRouter()

db = Database()


historias_repo = SqliteHistoriaClinicaRepository(db)


@router.get("/historias-clinicas")
def listar_historias_clinicas():
    return historias_repo.getAll()