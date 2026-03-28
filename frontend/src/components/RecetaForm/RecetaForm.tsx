import { useEffect, useState } from "react";
import { crearReceta } from "../../services/recetaService";
import { descargarPDF } from "../../services/recetaService";
import type { CrearRecetaDTO } from "../../services/recetaService";
import "./RecetaForm.css";

interface Paciente {
  id: number;
  nombre: string;
  apellido: string;
}

interface Medico {
  id: number;
  nombre: string;
  apellido: string;
}

interface Props {
  onCreated: () => void;
}

export default function RecetaForm({ onCreated }: Props) {
  const [pacientes, setPacientes] = useState<Paciente[]>([]);
  const [medicos, setMedicos] = useState<Medico[]>([]);

  const [form, setForm] = useState<CrearRecetaDTO>({
    paciente_id: 0,
    medico_id: 0,
    fecha_emision: "",
    detalle_medicamento: "",
    tratamiento: "",
  });

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/pacientes")
      .then((r) => r.json())
      .then((data) => setPacientes(data));

    fetch("http://127.0.0.1:8000/api/medicos")
      .then((r) => r.json())
      .then((data) => setMedicos(data));
  }, []);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setForm({
      ...form,
      [name]: name.includes("_id") ? Number(value) : value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      // 1️⃣ Crear receta en el backend
      const recetaCreada = await crearReceta(form);

      // 2️⃣ Descargar PDF con el ID devuelto
      descargarPDF(recetaCreada.receta_id);

      onCreated();

      // limpiar form
      setForm({
        paciente_id: 0,
        medico_id: 0,
        fecha_emision: "",
        detalle_medicamento: "",
        tratamiento: "",
      });

    } catch (error) {
      console.error(error);
      alert("Error al crear receta o descargar PDF");
    }
  };

  return (
    <div className="container mt-5">
      <div className="card shadow-lg p-4">
        <h2 className="text-center mb-4">📝 Nueva Receta</h2>

        <form onSubmit={handleSubmit}>
          <div className="row g-3">

            {/* PACIENTE */}
            <div className="col-md-6">
              <label className="form-label fw-bold">Paciente</label>
              <select
                className="form-select"
                name="paciente_id"
                value={form.paciente_id}
                onChange={handleChange}
              >
                <option value={0}>Seleccione un paciente</option>
                {pacientes.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.nombre} {p.apellido}
                  </option>
                ))}
              </select>
            </div>

            {/* MÉDICO */}
            <div className="col-md-6">
              <label className="form-label fw-bold">Médico</label>
              <select
                className="form-select"
                name="medico_id"
                value={form.medico_id}
                onChange={handleChange}
              >
                <option value={0}>Seleccione un médico</option>
                {medicos.map((m) => (
                  <option key={m.id} value={m.id}>
                    Dr. {m.nombre} {m.apellido}
                  </option>
                ))}
              </select>
            </div>

            {/* FECHA */}
            <div className="col-md-6">
              <label className="form-label fw-bold">Fecha de Emisión</label>
              <input
                type="date"
                className="form-control"
                name="fecha_emision"
                value={form.fecha_emision}
                onChange={handleChange}
              />
            </div>

            {/* DETALLE */}
            <div className="col-12">
              <label className="form-label fw-bold">Detalle del Medicamento</label>
              <textarea
                className="form-control"
                rows={3}
                name="detalle_medicamento"
                value={form.detalle_medicamento}
                onChange={handleChange}
              ></textarea>
            </div>

            {/* TRATAMIENTO */}
            <div className="col-12">
              <label className="form-label fw-bold">Tratamiento</label>
              <textarea
                className="form-control"
                rows={3}
                name="tratamiento"
                value={form.tratamiento}
                onChange={handleChange}
              ></textarea>
            </div>
          </div>

          <div className="d-grid mt-4">
            <button type="submit" className="btn btn-lg btn-calido-naranja">
              💊 Crear Receta y Descargar PDF
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
