import { useEffect, useState } from "react";
import { eliminarPaciente, listarPacientes } from "../../services/paciente.service";
import { PacienteForm } from "../PacienteForm/PacienteForm";
import type { Paciente } from "../../models/paciente";

export const PacienteList = () => {
  const [pacientes, setPacientes] = useState<Paciente[]>([]);
  const [editingMedicoId, setEditingMedicoId] = useState<number | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(true)
  

  const getPacientes = async () => {
    try { 
      const response = await listarPacientes();
      setPacientes(response);
      setLoading(false)
    } catch (error: any) {
      console.error("Error al listar pacientes", error);
      window.alert("Error al cargar los pacientes: " + error.message)
    }
  };

  useEffect(() => {
    getPacientes();
  }, []);

  const handleEliminar = async (id: number) => {
    if (window.confirm("¿Está seguro de eliminar el paciente?")) {
      try {
        await eliminarPaciente(id);
        setPacientes((prev) => prev.filter((m) => m.id !== id));
      } catch (error: any) {
        console.error("Error al eliminar paciente", error.message);
      }
    }
  };

  if (loading) {
    return(
      <h1>Cargando Pacientes...</h1>
    )
  }

  return (
    <>
      {/* Boton Para Crear el paciente */}
      <button
        className="btn btn-primary mb-3"
        onClick={() => {
          setShowForm(true);
          setEditingMedicoId(null);}}>
        Nuevo Médico
      </button>

      {/* Muestra el formulario si se selecciono para editar un paciente */}
      {showForm && (
        <PacienteForm
          pacienteId={editingMedicoId ?? undefined}
          onSuccess={() => {
            getPacientes();
            setShowForm(false);
            setEditingMedicoId(null);
          }}
          onCancel={() => {
            setShowForm(false);
            setEditingMedicoId(null);
          }}
        />
      )}
      {/* Tabla con los pacientes */}

      <table className="table table-striped table-hover shadow-sm">
        <thead className="table-primary">
          <tr>
            <th>Id</th>
            <th>Nombre</th>
            <th>Apellido</th>
            <th>Email</th>
            <th className="text-center">Acciones</th>
          </tr>
        </thead>
        <tbody>
          {pacientes.map((paciente) => (
            <tr key={paciente.id}>
              <td>{paciente.id}</td>
              <td>{paciente.nombre}</td>
              <td>{paciente.apellido}</td>
              <td>{paciente.email}</td>
              <td className="text-center">
                <button
                  className="btn btn-warning me-2"
                  onClick={() => {
                    setEditingMedicoId(paciente.id);
                    setShowForm(true);
                  }}
                >
                  Editar
                </button>
                <button
                  className="btn btn-danger"
                  onClick={() => handleEliminar(paciente.id)}
                >
                  Eliminar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
};