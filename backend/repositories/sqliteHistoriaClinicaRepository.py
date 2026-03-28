from interfaces.interfacePersistencia import IRepository 
from database import Database
from models.especialidad import Especialidad
from models.historiaClinica import HistoriaClinica
from models.medico import Medico
from models.paciente import Paciente

class SqliteHistoriaClinicaRepository(IRepository):
    def __init__(self, db: Database):
        self.db = db

    def getAll(self):
        query = """
            SELECT 
                hc.id, hc.fecha, hc.diagnostico, hc.tratamiento,

                -- Paciente
                p.id, p.nombre, p.apellido, p.email,

                -- Medico
                m.id, m.nombre, m.apellido, m.email,

                -- Especialidad del médico
                e.id, e.nombre, e.descripcion

            FROM historiales hc
            JOIN pacientes p ON hc.paciente_id = p.id
            JOIN medicos m ON hc.medico_id = m.id
            JOIN especialidades e ON m.especialidad_id = e.id
        """

        cursor = self.db.execute(query)
        filas = cursor.fetchall()

        historias = []

        for f in filas:
            (
                hc_id, fecha, diagnostico, tratamiento,
                pac_id, pac_nom, pac_ape, pac_mail,
                med_id, med_nom, med_ape, med_mail,
                esp_id, esp_nom, esp_desc
            ) = f

            paciente = Paciente(pac_id, pac_nom, pac_ape, pac_mail)
            especialidad = Especialidad(esp_id, esp_nom, esp_desc)
            medico = Medico(med_id, med_nom, med_ape, med_mail, especialidad)

            historia = HistoriaClinica(
                hc_id, medico, fecha, paciente, diagnostico, tratamiento
            )

            historias.append(historia)

        return historias

    def getById(self, id) -> HistoriaClinica:
        query = """
            SELECT 
                hc.id, hc.fecha, hc.diagnostico, hc.tratamiento,

                p.id, p.nombre, p.apellido, p.email,

                m.id, m.nombre, m.apellido, m.email,

                e.id, e.nombre, e.descripcion

            FROM historiales hc
            JOIN pacientes p ON hc.id_paciente = p.id
            JOIN medicos m ON hc.id_medico = m.id
            JOIN especialidades e ON m.especialidad_id = e.id
            WHERE hc.id = ?
        """

        cursor = self.db.execute(query, (id,))
        f = cursor.fetchone()

        if not f:
            return None

        (
            hc_id, fecha, diagnostico, tratamiento,
            pac_id, pac_nom, pac_ape, pac_mail,
            med_id, med_nom, med_ape, med_mail,
            esp_id, esp_nom, esp_desc
        ) = f

        paciente = Paciente(pac_id, pac_nom, pac_ape, pac_mail)
        especialidad = Especialidad(esp_id, esp_nom, esp_desc)
        medico = Medico(med_id, med_nom, med_ape, med_mail, especialidad)

        return HistoriaClinica(
            hc_id, medico, fecha, paciente, diagnostico, tratamiento
        )
    
    def getById(self, id):
        return super().getById(id)
    
    def save(self, historia: HistoriaClinica):
        query = """
            INSERT INTO historiales 
            (fecha, diagnostico, tratamiento, paciente_id, medico_id)
            VALUES (?, ?, ?, ?, ?)
        """

        self.db.execute(
            query,
            (
                historia.fecha,
                historia.diagnostico,
                historia.tratamiento,
                historia.paciente.id,
                historia.medico.id
            )
        )
    
    def update(self, historia: HistoriaClinica):
        query = """
            UPDATE historiales
            SET fecha = ?, diagnostico = ?, tratamiento = ?, 
                id_paciente = ?, id_medico = ?
            WHERE id = ?
        """

        self.db.execute(
            query,
            (
                historia.fecha,
                historia.diagnostico,
                historia.tratamiento,
                historia.paciente.id,
                historia.medico.id,
                historia.id
            )
        )
    
    def deleteById(self, id):
        return super().deleteById(id)
    