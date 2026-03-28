import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/historias-clinicas";

export const listarHistorias = async () => {
  try {
    const response = await axios.get(API_URL)
    return response.data
  } catch (error) {
    throw error;
  }
}