import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import type { PacienteBase } from "../../models/paciente";
import { actualizarPaciente, crearPaciente, obtenerPacientePorId } from "../../services/paciente.service";

interface PacienteFormProps {
  pacienteId?: number;
  onSuccess?: () => void;
  onCancel?: () => void;
}

export const PacienteForm = ({ pacienteId, onSuccess, onCancel }: PacienteFormProps) => {
  const { register, handleSubmit, reset } = useForm<PacienteBase>();
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      if (pacienteId) {
        try {
          const paciente = await obtenerPacientePorId(pacienteId);
          reset({
            nombre: paciente.nombre,
            apellido: paciente.apellido,
            email: paciente.email,
          });
        } catch (err) {
          console.error(err);
          setError("Error al cargar el paciente");
        }
      } else {
        reset({ nombre: "", apellido: "", email: "" });
      }
    };
    fetchData();
  }, [pacienteId, reset]);

  const onSubmit = async (data: PacienteBase) => {
    try {
      setError("");
      if (pacienteId) {
        await actualizarPaciente(pacienteId, data);
        window.alert("Paciente actualizado con éxito");
      } else {
        await crearPaciente(data);
        window.alert("Paciente creado con éxito");
      }
      reset();
      if (onSuccess) onSuccess();
    } catch (err) {
      console.error(err);
      window.alert("Error al guardar el paciente");
      setError("Error al guardar el paciente");
    }
  };

  return (
    <div className="card shadow-sm p-4 mb-4 mx-auto" style={{ maxWidth: "500px" }}>
      <h3 className="card-title mb-4 text-center">
        {pacienteId ? "Editar Paciente" : "Registrar Nuevo Paciente"}
      </h3>

      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="mb-3">
          <label className="form-label">Nombre</label>
          <input {...register("nombre")} className="form-control" required />
        </div>

        <div className="mb-3">
          <label className="form-label">Apellido</label>
          <input {...register("apellido")} className="form-control" required />
        </div>

        <div className="mb-3">
          <label className="form-label">Email</label>
          <input {...register("email")} type="email" className="form-control" required />
        </div>

        {error && <p className="text-danger mb-3">{error}</p>}

        <div className="d-flex justify-content-between">
          <button type="submit" className="btn btn-success">
            {pacienteId ? "Actualizar" : "Crear"}
          </button>

          {onCancel && (
            <button type="button" className="btn btn-secondary" onClick={onCancel}>
              Cancelar
            </button>
          )}
        </div>
      </form>
    </div>
  );
};
