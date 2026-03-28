import axios from "axios";
import type { Paciente, PacienteBase } from "../models/paciente";

const API_URL = "http://127.0.0.1:8000/api/pacientes";

export const crearPaciente = async (paciente: PacienteBase) => {
  try {
    console.log(paciente)
    const response = await axios.post(API_URL, paciente);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const listarPacientes = async () => {
  try {
    const response = await axios.get(API_URL)
    return response.data
  } catch (error) {
    throw error;
  }
}

export const eliminarPaciente = async(id: number) => {
  try {
    const response = await axios.delete(API_URL +`/${id}`)
    return response
  } catch (error) {
    throw error;
    
  }
}

export const obtenerPacientePorId = async (id: number) => {
  try {
    const response = await axios.get<Paciente>(`${API_URL}/${id}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const actualizarPaciente = async (id: number, pacienteData: Partial<PacienteBase>) => {
  try {
    const response = await axios.put(`${API_URL}/${id}`, pacienteData);
    return response.data;
  } catch (error) {
    throw error;
  }
};