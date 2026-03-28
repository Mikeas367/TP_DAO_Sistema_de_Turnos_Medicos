import { Link } from 'react-router-dom';
import './Sidebar.css';

import "bootstrap/dist/css/bootstrap.min.css";
import 'bootstrap/dist/js/bootstrap.bundle.min';

export const SideBar = () =>  {
    return(
    <>
    <div className="sidebar">
        <h1 className="sidebar-title">Menú</h1>

        <ul className="nav flex-colum">

            <li className='nav-item'>
                <Link to="/" className='nav-link'>
                    Inicio
                </Link>
            </li>

            {/* Médicos */}
            <li className='nav-item'>
                <Link to="/nuevo-medico" className='nav-link'>
                    <i className="bi bi-person-plus-fill"></i> Nuevo Medico
                </Link>
            </li>
            <li className='nav-item'>
                <Link to="/medicos" className='nav-link'>
                    <i className="bi bi-person-lines-fill"></i> Listado de Médicos
                </Link>
            </li>

            {/* Especialidades */}
            <li className='nav-item'>
                <Link to="/nueva-especialidad" className='nav-link'>
                    <i className="bi bi-plus-circle-fill"></i> Nueva Especialidad
                </Link>
            </li>
            
            <li className='nav-item'>
                <Link to="/especialidades" className='nav-link'>
                    <i className="bi bi-card-list"></i> Listado de Especialidades
                </Link>
            </li>
            

            {/* Turnos */}
            <li className='nav-item'>
                <Link to="/turnos" className='nav-link'>
                    <i className="bi bi-clipboard2-pulse-fill"></i> Turnos
                </Link>
            </li>
            <li className='nav-item'>
                <Link to="/turnos-medico" className='nav-link'>
                    <i className="bi bi-clipboard2-heart-fill"></i> Turnos de Médico
                </Link>
            </li>
            
            {/* <li className='nav-item'>
                <Link to="/nuevo-turno" className='nav-link'>
                    Nuevo Turno
                </Link>
            </li> */}
        

            {/* Agendas */}
            <li className='nav-item'>
                <Link to="/nueva-agenda" className='nav-link'>
                    <i className="bi bi-calendar-plus-fill"></i> Nueva Agenda
                </Link>
            </li>
            <li className='nav-item'>
                <Link to="/agendas" className='nav-link'>
                    <i className="bi bi-calendar-week-fill"></i> Agendas
                </Link>
            </li>

            {/* Pacientes */}
            <li className='nav-item'>
                <Link to="/nuevo-paciente" className='nav-link'>
                    <i className="bi bi-person-fill-add"></i> Nuevo Paciente
                </Link>
            </li>


            <li className='nav-item'>
                <Link to="/pacientes" className='nav-link'>
                    <i className="bi bi-person-lines-fill"></i> Listado de Pacientes
                </Link>
            </li>
            

            {/* Reportes */}
            <li className='nav-item'>
                <Link to="/reportes" className='nav-link'>
                    <i className="bi bi-bar-chart-line-fill"></i> Reportes
                </Link>
            </li>


            {/* Recetas */}
             <li className='nav-item'>
                <Link to="/recetas/nueva" className='nav-link'>
                    <i className="bi bi-clipboard2-plus-fill"></i> Nueva Receta
                </Link>
            </li>


            <li className='nav-item'>
                <Link to="/recetas" className='nav-link'>
                    <i className="bi bi-clipboard2-fill"></i> Recetas
                </Link>
            </li>


            <li className='nav-item'>
                <Link to="/historiales-clinicos" className='nav-link'>
                    <i className="bi bi-collection-fill"></i> Historiales Clinicos
                </Link>
            </li>


        </ul>
    </div>
    </>
    );
}

export default SideBar;
