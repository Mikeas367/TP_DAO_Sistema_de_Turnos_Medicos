import { useEffect, useState } from "react";
import type { HistorialClinico } from "../../models/historialClinico";
import type { Paciente } from "../../models/paciente";

import { listarHistorias } from "../../services/historialClinico.service";
import { listarPacientes } from "../../services/paciente.service";

export const HistoriaClinica = () => {
  const [historiales, setHistoriales] = useState<HistorialClinico[]>([]);
  const [pacientes, setPacientes] = useState<Paciente[]>([]);

  // Filtros
  const [pacienteId, setPacienteId] = useState<number | "">("");
  const [fechaDesde, setFechaDesde] = useState("");
  const [fechaHasta, setFechaHasta] = useState("");
  const [soloUltima, setSoloUltima] = useState(false);

  const cargarDatos = async () => {
    try {
      const [hcs, pacs] = await Promise.all([
        listarHistorias(),
        listarPacientes(),
      ]);

      setHistoriales(hcs);
      console.log(hcs)
      setPacientes(pacs);
    } catch (error: any) {
      window.alert("Error cargando datos: " + error.message);
    }
  };

  useEffect(() => {
    cargarDatos();
  }, []);

  /** 🔹 FILTRO PRINCIPAL */
  const filtrarHistoriales = () => {
    let resultados = [...historiales];

    // ----- Filtro por paciente -----
    if (pacienteId !== "") {
      resultados = resultados.filter((hc) => hc.paciente.id === pacienteId);
    }

    // Si los filtros de fechas están activos (solo si NO está "soloUltima")
    if (!soloUltima) {
      if (fechaDesde) {
        resultados = resultados.filter(
          (hc) => new Date(hc.fecha) >= new Date(fechaDesde)
        );
      }

      if (fechaHasta) {
        resultados = resultados.filter(
          (hc) => new Date(hc.fecha) <= new Date(fechaHasta)
        );
      }
    }

    // ----- Filtro "solo última historia clínica" -----
    if (soloUltima && pacienteId !== "") {
      if (resultados.length > 0) {
        resultados.sort(
          (a, b) =>
            new Date(b.fecha).getTime() -
            new Date(a.fecha).getTime()
        );
        return [resultados[0]]; // solo la última
      }
    }

    return resultados;
  };

  const historialesFiltrados = filtrarHistoriales();

  return (
    <>
      <h2 className="mb-4 fw-bold text-primary">Historial Clínico</h2>

      {/* Filtros */}
      <div className="card p-3 mb-4 shadow-sm">
        <h5 className="mb-3">Filtros</h5>

        <div className="row g-3">

          {/* Select de pacientes */}
          <div className="col-md-4">
            <label className="form-label">Paciente</label>
            <select
              className="form-select"
              value={pacienteId}
              onChange={(e) =>
                setPacienteId(e.target.value === "" ? "" : Number(e.target.value))
              }
            >
              <option value="">Todos</option>
              {pacientes.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.nombre} {p.apellido}
                </option>
              ))}
            </select>
          </div>

          {/* Checkbox: solo última HC */}
          <div className="col-md-3 d-flex align-items-end">
            <div className="form-check">
              <input
                className="form-check-input"
                type="checkbox"
                checked={soloUltima}
                onChange={() => setSoloUltima(!soloUltima)}
                disabled={pacienteId === ""} // solo habilitado si se eligió paciente
              />
              <label className="form-check-label">
                Mostrar solo última HC
              </label>
            </div>
          </div>

          {/* Filtro fechas */}
          <div className="col-md-2">
            <label className="form-label">Fecha desde</label>
            <input
              type="date"
              className="form-control"
              value={fechaDesde}
              onChange={(e) => setFechaDesde(e.target.value)}
              disabled={soloUltima}
            />
          </div>

          <div className="col-md-2">
            <label className="form-label">Fecha hasta</label>
            <input
              type="date"
              className="form-control"
              value={fechaHasta}
              onChange={(e) => setFechaHasta(e.target.value)}
              disabled={soloUltima}
            />
          </div>
        </div>
      </div>

      {/* Tabla */}
      <table className="table table-striped table-hover shadow-sm">
        <thead className="table-primary">
          <tr>
            <th>Nro Historia</th>
            <th>Médico</th>
            <th>Fecha</th>
            <th>Paciente</th>
            <th>Diagnóstico</th>
            <th>Tratamiento</th>
          </tr>
        </thead>

        <tbody>
          {historialesFiltrados.length > 0 ? (
            historialesFiltrados.map((hc) => (
              <tr key={hc.id}>
                <td>{hc.id}</td>
                <td>{hc.medico.nombre} {hc.medico.apellido}</td>
                <td>{hc.fecha}</td>
                <td>{hc.paciente.nombre} {hc.paciente.apellido}</td>
                <td>{hc.diagnostico}</td>
                <td>{hc.tratamiento}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={6} className="text-center text-muted py-3">
                No se encontraron resultados.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </>
  );
};
