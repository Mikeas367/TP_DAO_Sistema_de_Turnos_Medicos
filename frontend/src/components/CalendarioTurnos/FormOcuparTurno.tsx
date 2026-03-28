import React, { useEffect, useState } from "react";
import type { Turno } from "../../models/turno";
import type { Paciente } from "../../models/paciente";
import "./FormOcuparturno.css"

interface Props {
  turno: Turno | null;
  onClose: () => void;
  onConfirm: () => void;
}

export const FormOcuparTurno: React.FC<Props> = ({ turno, onClose, onConfirm }) => {
  const [pacientes, setPacientes] = useState<Paciente[]>([]);
  const [pacienteId, setPacienteId] = useState<number | "">("");

  
  if (!turno) return null;

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/pacientes")
      .then((res) => res.json())
      .then((data) => setPacientes(data))
      .catch((err) => console.error("Error cargando pacientes:", err));
  }, []);

  const fecha = new Date(turno.fecha.replace(" ", "T"));

  const handleSubmit = async () => {
    if (pacienteId === "") return;

    await fetch("http://127.0.0.1:8000/api/solicitar-turno", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        turno_id: turno.id,
        paciente_id: pacienteId,
      }),
    });

    onConfirm();
    onClose();
  };

  return (
    <div className="modal-bg">
      <div className="modal-card">
        <h3>Asignar Turno</h3>

        <p><b>Fecha:</b> {fecha.toLocaleString()}</p>
        <p><b>Médico:</b> {turno.medico.nombre} {turno.medico.apellido}</p>
        <p><b>Especialidad:</b> {turno.medico.especialidad.nombre}</p>

        <label>Paciente:</label>
        <select
          value={pacienteId}
          onChange={(e) => setPacienteId(Number(e.target.value))}
        >
          <option value="">Seleccionar...</option>
          {pacientes.map((p) => (
            <option key={p.id} value={p.id}>
              {p.nombre} {p.apellido}
            </option>
          ))}
        </select>

        <button onClick={handleSubmit}>Confirmar</button>
        <button onClick={onClose}>Cancelar</button>
      </div>
    </div>
  );
};