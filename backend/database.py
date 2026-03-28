import sqlite3

class Database:
    def __init__(self, db_name="medicos.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):

        # ==========================
        #   TABLA ESPECIALIDADES
        # ==========================
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS especialidades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL, 
                descripcion TEXT NOT NULL   
            )
        ''')

        # ==========================
        #   TABLA MEDICOS
        # ==========================
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                email TEXT UNIQUE,
                especialidad_id INTEGER NOT NULL,
                FOREIGN KEY (especialidad_id) REFERENCES especialidades(id)
            )
        ''')

        # ==========================
        #   TABLA PACIENTES
        # ==========================
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                email TEXT UNIQUE
            )
        ''')

        # ==========================
        #   TABLA ESTADOS
        # ==========================
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS estados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT
            )
        ''')

        # ==========================
        #   TABLA TURNOS
        # ==========================
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS turnos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER,
                medico_id INTEGER NOT NULL,
                estado_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
                FOREIGN KEY (medico_id) REFERENCES medicos(id),
                FOREIGN KEY (estado_id) REFERENCES estados(id)
            )
        ''')

        # ==========================
        #   TABLA RECETAS
        # ==========================
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS recetas (
                receta_id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                medico_id INTEGER NOT NULL,
                fecha_emision TEXT NOT NULL,
                detalle_medicamento TEXT NOT NULL,
                tratamiento TEXT NOT NULL,
                FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
                FOREIGN KEY (medico_id) REFERENCES medicos(id)
            )
        ''')

        # ==========================
        #   TABLA HISTORIALES
        # ==========================
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS historiales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                medico_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                paciente_id INTEGER NOT NULL,
                diagnostico TEXT NOT NULL,
                tratamiento TEXT NOT NULL,
                FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
                FOREIGN KEY (medico_id) REFERENCES medicos(id)
            )
        ''')

        # ==========================
        #   TABLA AGENDAS MEDICO
        # ==========================
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS agendas_medico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                medico_id INTEGER NOT NULL,
                FOREIGN KEY (medico_id) REFERENCES medicos(id)
            )
        ''')

        # ==========================
        #   TABLA DIAS LABORABLES
        # ==========================
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS agenda_dias_trabajo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agenda_id INTEGER NOT NULL,
                dia_semana INTEGER NOT NULL,       
                hora_inicio TEXT NOT NULL,         
                hora_fin TEXT NOT NULL,            
                duracion_turno_min INTEGER NOT NULL,
                FOREIGN KEY (agenda_id) REFERENCES agendas_medico(id)
            )
        ''')

        self.conn.commit()

    def execute(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()
        return self.cursor
