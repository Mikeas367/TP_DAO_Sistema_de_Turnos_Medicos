import { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import { 
  MedicoForm, 
  MedicoList, 
  SideBar 
} from "./components";

import { TurnosForm } from "./components/CalendarioTurnos/TurnosForm";
import { EspecialidadList } from "./components/EspecialidadList/EspecialidadList";
import { EspecialidadForm } from "./components/EspecialidadForm/EspecialidadForm";
import { MedicoTurnos } from "./components/MedicoTurno/MedicoTurnos";
//import { NuevoTurnoForm } from "./components/TurnoForm/NuevoTurnoForm";

import { AgendaForm } from "./components/AgendaForm/AgendaForm";
import { AgendaList } from "./components/AgendaList/AgendaList";

import { Reportes } from "./components/Reportes/Reportes";

import RecetaList from "./components/RecetaList/RecetaList";
import RecetaForm from "./components/RecetaForm/RecetaForm";

import { PacienteForm } from "./components/PacienteForm/PacienteForm";
import { PacienteList } from "./components/PacienteList/PacienteList";

import { obtenerRecetas } from "./services/recetaService";
import type { Receta } from "./services/recetaService";

import "bootstrap-icons/font/bootstrap-icons.css";
import { HistoriaClinica } from "./components/HistorialClinico/HistorialClinico";

function App() {

  // ============================
  // ESTADO DE RECETAS
  // ============================

  const [recetas, setRecetas] = useState<Receta[]>([]);

  const cargarRecetas = async () => {
    try {
      const data = await obtenerRecetas();
      setRecetas(data);
    } catch (error) {
      console.error("Error cargando recetas:", error);
    }
  };

  useEffect(() => {
    cargarRecetas();
  }, []);


  return (
    <Router>
      <SideBar />

      <div className="content" style={{ marginLeft: "260px", padding: "20px" }}>
        <Routes>

          {/* =======================
              RUTAS PRINCIPALES
          ======================== */}
          <Route path="/" element={<h1>Bienvenido</h1>} />

          <Route path="/nuevo-medico" element={<MedicoForm />} />
          <Route path="/medicos" element={<MedicoList />} />

          <Route path="/turnos" element={<TurnosForm />} />
          <Route path="/turnos-medico" element={<MedicoTurnos />} />

          {/* <Route path="/nuevo-turno" element={<NuevoTurnoForm />} /> */}

          <Route path="/especialidades" element={<EspecialidadList />} />
          <Route path="/nueva-especialidad" element={<EspecialidadForm />} />

          {/* =======================
              PACIENTES
          ======================== */}
          <Route path="/nuevo-paciente" element={<PacienteForm />} />
          <Route path="/pacientes" element={<PacienteList />} />

          {/* =======================
              AGENDAS
          ======================== */}
          <Route path="/nueva-agenda" element={<AgendaForm />} />
          <Route path="/agendas" element={<AgendaList />} />

          {/* =======================
              REPORTES
          ======================== */}
          <Route path="/reportes" element={<Reportes />} />

          {/* =======================
              RECETAS
          ======================== */}
          <Route 
            path="/recetas" 
            element={<RecetaList recetas={recetas} />} 
          />

          <Route 
            path="/recetas/nueva" 
            element={<RecetaForm onCreated={cargarRecetas} />} 
          />

          <Route 
            path="/historiales-clinicos" 
            element={<HistoriaClinica/>} 
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
