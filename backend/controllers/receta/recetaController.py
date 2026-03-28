from repositories.sqliteRecetaRepository import SqliteRecetaRepository
from utils.pdf_generator import generar_receta_pdf

class RecetaController:
    def __init__(self):
        self.repo_class = SqliteRecetaRepository

    def crear_receta_controller(self, db, receta):
        repo = self.repo_class(db)

        # repo.crear_receta ahora debe devolver TODOS los datos
        db_receta = repo.crear_receta(receta)

        # Pasamos el dict completo al generador PDF
        generar_receta_pdf(db_receta)

        return db_receta

    def listar_recetas_controller(self, db):
        repo = self.repo_class(db)
        return repo.listar_recetas()

recetacontroller = RecetaController()
