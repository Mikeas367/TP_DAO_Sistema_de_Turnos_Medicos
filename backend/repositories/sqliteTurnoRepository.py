from interfaces.interfacePersistencia import IRepository
from models.medico import Medico
from database import Database
from models.especialidad import Especialidad
from models.turno import Turno
from models.paciente import Paciente
from models.estado import Estado

class SqliteTurnoRepository(IRepository):
    def __init__(self, db: Database):
        self.db = db

    # ----------------------------------------------------------------------
    # SAVE
    # ----------------------------------------------------------------------
    def save(self, turno: Turno):
        query = """
            INSERT INTO turnos (fecha, paciente_id, medico_id, estado_id)
            VALUES (?, ?, ?, ?)
        """
        
        paciente_id = turno.paciente.id if turno.paciente else None

        self.db.execute(
            query,
            (
                turno.fecha,
                paciente_id,
                turno.medico.id,
                turno.estado.id
            )
        )

    # ----------------------------------------------------------------------
    # GET ALL
    # ----------------------------------------------------------------------
    def getAll(self):
        query = """
        SELECT 
            t.id, t.fecha,

            p.id, p.nombre, p.apellido, p.email,

            m.id, m.nombre, m.apellido, m.email,

            e.id, e.nombre, e.descripcion,

            est.id, est.nombre, est.descripcion

        FROM turnos t
        LEFT JOIN pacientes p ON t.paciente_id = p.id
        JOIN medicos m ON t.medico_id = m.id
        JOIN especialidades e ON m.especialidad_id = e.id
        JOIN estados est ON t.estado_id = est.id
        """

        cursor = self.db.execute(query)
        filas = cursor.fetchall()

        turnos = []
        for f in filas:
            (
                turno_id, fecha,
                pac_id, pac_nom, pac_ape, pac_mail,
                med_id, med_nom, med_ape, med_mail,
                esp_id, esp_nom, esp_desc,
                est_id, est_nom, est_desc
            ) = f

            paciente = Paciente(pac_id, pac_nom, pac_ape, pac_mail) if pac_id else None

            especialidad = Especialidad(esp_id, esp_nom, esp_desc)
            medico = Medico(med_id, med_nom, med_ape, med_mail, especialidad)
            estado = Estado(est_id, est_nom, est_desc)

            turno = Turno(turno_id, paciente, medico, estado, fecha)
            turnos.append(turno)

        return turnos

    # ----------------------------------------------------------------------
    # GET BY ID
    # ----------------------------------------------------------------------
    def getById(self, id) -> Turno:
        query = """
        SELECT 
            t.id, t.fecha,

            p.id, p.nombre, p.apellido, p.email,

            m.id, m.nombre, m.apellido, m.email,

            e.id, e.nombre, e.descripcion,

            est.id, est.nombre, est.descripcion

        FROM turnos t
        LEFT JOIN pacientes p ON t.paciente_id = p.id
        JOIN medicos m ON t.medico_id = m.id
        JOIN especialidades e ON m.especialidad_id = e.id
        JOIN estados est ON t.estado_id = est.id
        WHERE t.id = ?
        """

        cursor = self.db.execute(query, (id,))
        f = cursor.fetchone()

        if not f:
            return None

        (
            turno_id, fecha,
            pac_id, pac_nom, pac_ape, pac_mail,
            med_id, med_nom, med_ape, med_mail,
            esp_id, esp_nom, esp_desc,
            est_id, est_nom, est_desc
        ) = f

        paciente = Paciente(pac_id, pac_nom, pac_ape, pac_mail) if pac_id else None

        especialidad = Especialidad(esp_id, esp_nom, esp_desc)
        medico = Medico(med_id, med_nom, med_ape, med_mail, especialidad)
        estado = Estado(est_id, est_nom, est_desc)

        return Turno(turno_id, paciente, medico, estado, fecha)

    # ----------------------------------------------------------------------
    # UPDATE
    # ----------------------------------------------------------------------
    def update(self, turno: Turno):
        query = """
            UPDATE turnos
            SET paciente_id = ?, medico_id = ?, estado_id = ?, fecha = ?
            WHERE id = ?
        """
        paciente_id = turno.paciente.id if turno.paciente else None

        self.db.execute(query, (
            paciente_id,
            turno.medico.id,
            turno.estado.id,
            turno.fecha,
            turno.id
        ))

    # ----------------------------------------------------------------------
    # DELETE
    # ----------------------------------------------------------------------
    def deleteById(self, id):
        pass

    # ----------------------------------------------------------------------
    # REPORTES
    # ----------------------------------------------------------------------

    ## Pacientes atendidos entre fechas
    def getPacientesAtendidos(self, desde, hasta):
        query = """
            SELECT 
                t.id, t.fecha,
                p.id, p.nombre, p.apellido, p.email,
                m.id, m.nombre, m.apellido, m.email,
                e.id, e.nombre, e.descripcion,
                est.id, est.nombre, est.descripcion

            FROM turnos t
            JOIN pacientes p ON t.paciente_id = p.id
            JOIN medicos m ON t.medico_id = m.id
            JOIN especialidades e ON m.especialidad_id = e.id
            JOIN estados est ON t.estado_id = est.id
            WHERE t.fecha BETWEEN ? AND ?
            ORDER BY t.fecha ASC
        """

        cursor = self.db.execute(query, (desde, hasta))
        rows = cursor.fetchall()

        turnos = []
        for r in rows:
            (
                turno_id, fecha,
                pac_id, pac_nombre, pac_apellido, pac_email,
                med_id, med_nombre, med_apellido, med_email,
                esp_id, esp_nombre, esp_desc,
                est_id, est_nombre, est_desc
            ) = r

            turnos.append({
                "id": turno_id,
                "fecha": fecha,
                "paciente_id": pac_id,
                "nombre": pac_nombre,
                "apellido": pac_apellido,
                "email": pac_email,
                "medico": f"{med_nombre} {med_apellido}",
                "especialidad": esp_nombre,
                "estado": est_nombre
            })

        return turnos

    ## Turnos por rango simple
    def getByFecha(self, desde, hasta):
        query = """
            SELECT id, paciente_id, medico_id, fecha, asistido
            FROM turnos
            WHERE fecha BETWEEN ? AND ?
        """

        cursor = self.db.execute(query, (desde, hasta))
        filas = cursor.fetchall()

        turnos = []
        for f in filas:
            turnos.append(Turno(
                id=f[0],
                paciente_id=f[1],
                medico_id=f[2],
                fecha=f[3],
                asistido=f[4]
            ))
        return turnos

    ## Asistencias / Inasistencias
    def obtener_asistencias_inasistencias(self, desde, hasta):
        query = """
            SELECT 
                SUM(CASE WHEN estado_id = 3 THEN 1 ELSE 0 END) AS asistencias,
                SUM(CASE WHEN estado_id = 4 THEN 1 ELSE 0 END) AS inasistencias
            FROM turnos
            WHERE fecha BETWEEN ? AND ?
        """
        cursor = self.db.execute(query, (desde, hasta))
        return cursor.fetchone()

    ## Turnos por fecha para reporte de especialidad
    def getTurnosEntreFechas(self, desde, hasta):
        query = """
            SELECT 
                t.id,
                t.paciente_id,
                t.medico_id,
                t.estado_id,
                t.fecha,
                m.nombre AS medico_nombre,
                e.nombre AS especialidad_nombre
            FROM turnos t
            JOIN medicos m ON t.medico_id = m.id
            JOIN especialidades e ON m.especialidad_id = e.id
            WHERE t.fecha BETWEEN ? AND ?
        """

        filas = self.db.execute(query, (desde, hasta))

        turnos = []
        for row in filas:
            turnos.append(self.mapear_turno_fecha(row))

        return turnos

    ## Mapper para el reporte
    def mapear_turno_fecha(self, fila):
        especialidad = Especialidad(
            id=None,
            nombre=fila[6],
            descripcion=None
        )

        medico = Medico(
            id=fila[2],
            nombre=fila[5],
            apellido="",
            email="",
            especialidad=especialidad
        )

        estado = Estado(
            id=fila[3],
            nombre="",
            descripcion=""
        )

        paciente = Paciente(
            id=fila[1],
            nombre="",
            apellido="",
            email=""
        )

        return Turno(
            id=fila[0],
            paciente=paciente,
            medico=medico,
            estado=estado,
            fecha=fila[4]
        )
