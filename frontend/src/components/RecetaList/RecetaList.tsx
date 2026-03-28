import { useEffect, useState } from "react";
import type { Receta } from "../../services/recetaService";
import "bootstrap/dist/css/bootstrap.min.css";
import "./RecetaList.css";

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
    recetas: Receta[];
}

export default function RecetaList({ recetas }: Props) {
    const [recetaAbierta, setRecetaAbierta] = useState<number | null>(null);
    const [pacientes, setPacientes] = useState<Paciente[]>([]);
    const [medicos, setMedicos] = useState<Medico[]>([]);

    useEffect(() => {
        fetch("http://127.0.0.1:8000/api/pacientes")
            .then(r => r.json())
            .then(data => setPacientes(data));

        fetch("http://127.0.0.1:8000/api/medicos")
            .then(r => r.json())
            .then(data => setMedicos(data));
    }, []);

    const getPacienteNombre = (id: number) => {
        const p = pacientes.find(x => x.id === id);
        return p ? `${p.nombre} ${p.apellido}` : "Desconocido";
    };

    const getMedicoNombre = (id: number) => {
        const m = medicos.find(x => x.id === id);
        return m ? `Dr. ${m.nombre} ${m.apellido}` : "Desconocido";
    };

    return (
        <div className="container mt-4">
            <h2 className="text-center mb-4">📋 Listado de Recetas</h2>

            {recetas.length === 0 ? (
                <p className="text-center text-muted">No hay recetas cargadas.</p>
            ) : (
                <div className="row g-4">
                    {recetas.map((r) => (
                        <div key={r.receta_id} className="col-md-6">
                            <div className="card shadow-sm">
                                <div className="card-body">
                                    <h5 className="card-title">
                                        🧾 Receta #{r.receta_id}
                                    </h5>

                                    <p className="card-text">
                                        <strong>Paciente:</strong>{" "}
                                        {getPacienteNombre(r.paciente_id)}
                                    </p>

                                    <button
                                        className="btn btn-calido-naranja w-100"
                                        onClick={() =>
                                            setRecetaAbierta(
                                                recetaAbierta === r.receta_id ? null : r.receta_id
                                            )
                                        }
                                    >
                                        {recetaAbierta === r.receta_id
                                            ? "Ocultar detalles"
                                            : "Ver detalles"}
                                    </button>

                                    {recetaAbierta === r.receta_id && (
                                        <div className="mt-3">
                                            <hr />
                                            <p>
                                                <strong>Médico:</strong>{" "}
                                                {getMedicoNombre(r.medico_id)}
                                            </p>
                                            <p>
                                                <strong>Fecha de emisión:</strong>{" "}
                                                {r.fecha_emision}
                                            </p>
                                            <p>
                                                <strong>Medicamento:</strong>{" "}
                                                {r.detalle_medicamento}
                                            </p>
                                            <p>
                                                <strong>Tratamiento:</strong>{" "}
                                                {r.tratamiento}
                                            </p>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
