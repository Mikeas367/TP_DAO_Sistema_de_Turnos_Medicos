import React from "react";
import type { Turno } from "../../models/turno";
import "./Calendario.css"

interface Props{
  turnos: Turno[];
  onSeleccionar: (turno: Turno) => void;      // Para ocupar turno
  onLiberar: (turno: Turno) => void;          // Para liberar turno
}

export const CalendarTurnos: React.FC<Props> = ({ turnos, onSeleccionar, onLiberar }) => {
  return (
    <div className="calendar-container">
      {turnos.map((turno) => {
        const fecha = new Date(turno.fecha);
        const esOcupado = turno.estado.nombre === "Ocupado";

        return (
          <div
            key={turno.id}
            className={`turno-card ${esOcupado ? "ocupado" : "libre"}`}
            onClick={() => !esOcupado && onSeleccionar(turno)}
            style={{ cursor: esOcupado ? "default" : "pointer" }}
          >
            <strong>
              {fecha.toLocaleDateString()} - {fecha.getHours()}:{fecha.getMinutes()}
            </strong>

            <p>
              <b>Médico:</b> {turno.medico.nombre} {turno.medico.apellido}
            </p>

            <p>
              <b>Especialidad:</b> {turno.medico.especialidad.nombre}
            </p>

            {turno.paciente ? (
              <>
                <p>
                  <b>Paciente:</b> {turno.paciente.nombre} {turno.paciente.apellido}
                </p>

                {/* BOTÓN LIBERAR TURNO */}
                <button
                  className="btn-liberar"
                  onClick={(e) => {
                    e.stopPropagation();   // evita abrir modal
                    onLiberar(turno);
                  }}
                >
                  Liberar turno
                </button>
              </>
            ) : (
              <p className="sin-paciente">Sin paciente</p>
            )}
          </div>
        );
      })}
    </div>
  );
};