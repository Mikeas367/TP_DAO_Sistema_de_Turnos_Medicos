import React, { useState } from "react";
import "./Reportes.css";

export const Reportes: React.FC = () => {
  const [desde, setDesde] = useState<string>("");
  const [hasta, setHasta] = useState<string>("");

  const descargarPDF = (
    endpoint: "pacientes" | "asistencias" | "especialidad"
  ) => {
    if (!desde || !hasta) {
      alert("Seleccioná las fechas primero");
      return;
    }

    let url = "";

    if (endpoint === "pacientes") {
      url = `http://127.0.0.1:8000/api/pacientes-atendidos-pdf?desde=${desde}&hasta=${hasta}`;
    } else if (endpoint === "asistencias") {
      url = `http://127.0.0.1:8000/api/asistencia-vs-inasistencias-pdf?desde=${desde}&hasta=${hasta}`;
    } else if (endpoint === "especialidad") {
      url = `http://127.0.0.1:8000/api/turno_x_especialidad_pdf?desde=${desde}&hasta=${hasta}`;
    }

    window.open(url, "_blank");
  };

  return (
    <div className="container mt-5">
      <div className="card shadow-lg p-4">
        <h2 className="text-center mb-4">📊 Reportes</h2>

        <div className="row g-3 mb-4">
          <div className="col-md-6">
            <label className="form-label fw-bold">Desde</label>
            <input
              type="date"
              className="form-control"
              value={desde}
              onChange={(e) => setDesde(e.target.value)}
            />
          </div>

          <div className="col-md-6">
            <label className="form-label fw-bold">Hasta</label>
            <input
              type="date"
              className="form-control"
              value={hasta}
              onChange={(e) => setHasta(e.target.value)}
            />
          </div>
        </div>

        <div className="d-grid gap-3">
          <button
            className="btn btn-lg btn-calido-naranja"
            onClick={() => descargarPDF("pacientes")}
          >
            <i className="bi bi-file-pdf-fill"></i> PDF — Pacientes Atendidos 
          </button>

          <button
            className="btn btn-lg btn-calido-coral"
            onClick={() => descargarPDF("asistencias")}
          >
            <i className="bi bi-file-pdf-fill"></i> PDF — Asistencias / Inasistencias 
          </button>

          <button
            className="btn btn-lg btn-calido-amarillo"
            onClick={() => descargarPDF("especialidad")}
          >
            <i className="bi bi-file-pdf-fill"></i> PDF — Turnos por Especialidad 
          </button>
        </div>
      </div>
    </div>
  );
};
