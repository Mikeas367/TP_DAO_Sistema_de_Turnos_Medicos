from interfaces.interfacePersistencia import IRepository 
from database import Database
from models.paciente import Paciente


class SqlitePacienteRepository(IRepository):
    def __init__(self, db: Database):
        self.db = db

    def save(self, paciente: Paciente):
        query = "INSERT INTO pacientes (nombre, apellido, email) VALUES (?, ?, ?) "
        self.db.execute(query, (paciente.nombre, paciente.apellido, paciente.email))

    def getAll(self):
        print("ENtRO AL GETALL")
        query = """
            SELECT p.id, p.nombre, p.apellido, p.email
            FROM pacientes p
        """
        cursor = self.db.execute(query)
        filas = cursor.fetchall()
        pacientes = []
        for f in filas:
            esp = Paciente(f[0], f[1], f[2], f[3])
            pacientes.append(esp)

        return pacientes
    
    def getById(self, id):
        query = "SELECT id, nombre, apellido, email FROM pacientes WHERE id = ?"
        cursor = self.db.execute(query, (id,))
        fila = cursor.fetchone()

        if not fila:
            return None

        return Paciente(
            id=fila[0],
            nombre=fila[1],
            apellido=fila[2],
            email=fila[3],
        )

    def update(self, paciente: Paciente):
        pass
        

    def deleteById(self, id):
        query = "DELETE FROM pacientes WHERE id = ?"
        cursor = self.db.execute(query, (id,))
        return cursor.rowcount > 0

        
