from datetime import date, timedelta
from interfaces.interfacePersistencia import IRepository


class GeneradorTurnosController:
    def __init__(self, agenda_repo: IRepository, turnos_repo: IRepository, estado_repo: IRepository):
        self.agenda_repo = agenda_repo
        self.turnos_repo = turnos_repo
        self.estado_repo = estado_repo
    
    
    def buscar_estado_libre(self):
        estados = self.estado_repo.getAll()
        for e in estados:
            if e.es_libre():
                return e
    

    def buscar_agenda_por_id(self, id:int):
        agenda = self.agenda_repo.getById(id)
        return agenda

    def generar_turnos_de_agenda(self, id:int):
        agenda = self.buscar_agenda_por_id(id)
        estado_libre = self.buscar_estado_libre()
        turnos = self.turnos_repo.getAll()
        fecha_desde = date.today()
        fecha_hasta = fecha_desde + timedelta(days=10)
        
        turnos_generados = agenda.generar_turnos(fecha_desde, fecha_hasta, estado_libre)

        for turno in turnos_generados:
            self.turnos_repo.save(turno)
