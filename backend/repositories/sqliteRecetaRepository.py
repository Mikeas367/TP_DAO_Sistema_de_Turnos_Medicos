class SqliteRecetaRepository:
    def __init__(self, db):
        self.db = db

    def crear_receta(self, receta):
        # 1) Insertar receta
        query = '''
            INSERT INTO recetas (
                paciente_id, medico_id,
                fecha_emision, detalle_medicamento, tratamiento
            )
            VALUES (?, ?, ?, ?, ?)
        '''
        self.db.cursor.execute(query, (
            receta.paciente_id,
            receta.medico_id,
            receta.fecha_emision,
            receta.detalle_medicamento,
            receta.tratamiento
        ))

        receta_id = self.db.cursor.lastrowid

        # 2) ─ Obtener datos del paciente
        self.db.cursor.execute(
            "SELECT nombre, apellido FROM pacientes WHERE id = ?",
            (receta.paciente_id,)
        )
        paciente = self.db.cursor.fetchone()
        paciente_nombre = paciente[0] if paciente else ""
        paciente_apellido = paciente[1] if paciente else ""

        # 3) ─ Obtener datos del médico
        self.db.cursor.execute(
            "SELECT nombre, apellido FROM medicos WHERE id = ?",
            (receta.medico_id,)
        )
        medico = self.db.cursor.fetchone()
        medico_nombre = medico[0] if medico else ""
        medico_apellido = medico[1] if medico else ""

        # 4) ─ Devolver receta completa lista para el PDF
        return {
            "receta_id": receta_id,
            "paciente_id": receta.paciente_id,
            "paciente_nombre": paciente_nombre,
            "paciente_apellido": paciente_apellido,
            "medico_id": receta.medico_id,
            "medico_nombre": medico_nombre,
            "medico_apellido": medico_apellido,
            "fecha_emision": receta.fecha_emision,
            "detalle_medicamento": receta.detalle_medicamento,
            "tratamiento": receta.tratamiento
        }

    # ============================================================

    def obtener_recetas(self):
        query = '''
            SELECT 
                r.receta_id,
                r.paciente_id,
                p.nombre AS paciente_nombre,
                p.apellido AS paciente_apellido,
                r.medico_id,
                m.nombre AS medico_nombre,
                m.apellido AS medico_apellido,
                r.fecha_emision,
                r.detalle_medicamento,
                r.tratamiento
            FROM recetas r
            LEFT JOIN pacientes p ON r.paciente_id = p.id
            LEFT JOIN medicos m ON r.medico_id = m.id
        '''
        self.db.cursor.execute(query)
        rows = self.db.cursor.fetchall()

        recetas = []
        for r in rows:
            recetas.append({
                "receta_id": r[0],
                "paciente_id": r[1],
                "paciente_nombre": r[2] or "",
                "paciente_apellido": r[3] or "",
                "medico_id": r[4],
                "medico_nombre": r[5] or "",
                "medico_apellido": r[6] or "",
                "fecha_emision": r[7],
                "detalle_medicamento": r[8],
                "tratamiento": r[9]
            })

        return recetas

    def listar_recetas(self):
        return self.obtener_recetas()