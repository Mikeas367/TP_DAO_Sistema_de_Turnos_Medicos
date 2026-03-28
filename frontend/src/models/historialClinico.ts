import type { Medico } from "./medico";
import type { Paciente } from "./paciente";

export interface HistorialClinico{
    id: number,
    medico: Medico,
    fecha: string,
    paciente: Paciente,
    diagnostico: string,
    tratamiento: string
}
