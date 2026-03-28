import { useState, useEffect } from "react";
import type { Turno } from "../../models/turno";
import { CalendarTurnos } from "./CalendarioTurnos";
import { FormOcuparTurno } from "./FormOcuparTurno";

export const TurnosForm = () => {
  const [turnos, setTurnos] = useState<Turno[]>([]);
  const [fechaFiltro, setFechaFiltro] = useState<string>("");
  const [espFiltro, setEspFiltro] = useState<number | "">("");
  const [turnoSeleccionado, setTurnoSeleccionado] = useState<Turno | null>(null);
  const [estadoFiltro, setEstadoFiltro] = useState<string>("");

  const cargarTurnos = () => {
    fetch("http://127.0.0.1:8000/api/turnos")
      .then((res) => res.json())
      .then((data) => setTurnos(data));
  };

  useEffect(() => {
    cargarTurnos();
  }, []);

  // ----------------------------- 
  // ESPECIALIDADES ÚNICAS
  // -----------------------------
  const especialidades = Array.from(
    new Map(
      turnos.map((t) => [t.medico.especialidad.id, t.medico.especialidad.nombre])
    ).entries()
  );

  // ----------------------------- 
  // FILTRO DE TURNOS
  // -----------------------------
  const turnosFiltrados = turnos.filter((t) => {
    const coincideFecha = fechaFiltro
      ? new Date(t.fecha.replace(" ", "T")) >= new Date(fechaFiltro)
      : true;

    const coincideEsp = espFiltro
      ? t.medico.especialidad.id === espFiltro
      : true;
    
    const coincideEstado = estadoFiltro
      ? t.estado.nombre === estadoFiltro
      : true;

    return coincideFecha && coincideEsp && coincideEstado;
  });

  // ----------------------------- 
  // LIBERAR TURNO (POST)
  // -----------------------------
  const liberarTurno = async (turno: Turno) => {
    const body = {
      turno_id: turno.id,
      paciente_id: turno.paciente?.id ?? 0,
    };

    await fetch("http://127.0.0.1:8000/api/liberar-turno", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    cargarTurnos();
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Calendario de Turnos</h1>

      {/* FILTROS */}
      <div style={{ display: "flex", gap: "20px", marginBottom: "20px" }}>
        <div>
          <label>Filtrar por fecha:</label><br />
          <input
            type="date"
            value={fechaFiltro}
            onChange={(e) => setFechaFiltro(e.target.value)}
          />
        </div>

        <div>
          <label>Filtrar por especialidad:</label><br />
          <select
            value={espFiltro}
            onChange={(e) =>
              setEspFiltro(e.target.value ? Number(e.target.value) : "")
            }
          >
            <option value="">Todas</option>
            {especialidades.map(([id, nombre]) => (
              <option key={id} value={id}>{nombre}</option>
            ))}
          </select>
        </div>
      </div>

      <div>
          <label>Filtrar por estado:</label><br />
          <select
            value={estadoFiltro}
            onChange={(e) => setEstadoFiltro(e.target.value)}
          >
            <option value="">Todos</option>
            <option value="Libre">Disponibles</option>
            <option value="Ocupado">Ocupados</option>
          </select>
      </div>

      {/* CALENDARIO */}
      <CalendarTurnos
        turnos={turnosFiltrados}
        onSeleccionar={(t) => setTurnoSeleccionado(t)}
        onLiberar={liberarTurno}     // <<<<<< NUEVO
      />

      {/* MODAL */}
      {turnoSeleccionado && (
        <FormOcuparTurno
          turno={turnoSeleccionado}
          onClose={() => setTurnoSeleccionado(null)}
          onConfirm={() => cargarTurnos()}
        />
      )}
    </div>
  );
};
