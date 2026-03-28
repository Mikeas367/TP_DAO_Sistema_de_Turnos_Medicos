export interface Receta {
    receta_id: number;
    paciente_id: number;
    medico_id: number;
    fecha_emision: string;
    detalle_medicamento: string;
    tratamiento: string;
}

export interface CrearRecetaDTO {
    paciente_id: number;
    medico_id: number;
    fecha_emision: string;
    detalle_medicamento: string;
    tratamiento: string;
}

const API_URL = "http://localhost:8000/api/recetas";

// Obtener todas las recetas
export async function obtenerRecetas(): Promise<Receta[]> {
    const res = await fetch(API_URL);

    if (!res.ok) {
        throw new Error("Error al obtener recetas");
    }

    return await res.json();
}

// Crear una receta
export async function crearReceta(data: CrearRecetaDTO): Promise<Receta> {
    const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });

    if (!res.ok) {
        throw new Error("Error al crear receta");
    }

    return await res.json();
}

// Descargar PDF
export function descargarPDF(receta_id: number): void {
    window.open(`${API_URL}/${receta_id}/pdf`, "_blank");
}
