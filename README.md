# 🩺 Sistema Gestion de Turnos para Medicos
Trabajo practico de la materia "Desarrollo de Aplicaciones con Objetos", en este trabajo practico grupal se realizo un sistema que facilitaria a los medicos y a los admistrativos la gestion de agendas, turnos, pacientes, historiales clinicos como ademas la generacion de distintos reportes y estadisticas.

# 💼 Enunciado proporcionado 
### **Sistema de Turnos Médicos**
**Funcionalidades Principales:**
* ABM de pacientes, médicos y especialidades.
* Registro de turnos (paciente + médico + fecha + estado).
* Validación de horarios disponibles para evitar superposición de turnos.
* Módulo de historial clínico de pacientes.
* Emisión de recetas electrónicas.

**Reportes Requeridos:**
* Listado de turnos por médico en un período.
* Cantidad de turnos por especialidad.
* Pacientes atendidos en un rango de fechas.
* Gráfico estadístico: asistencia vs. inasistencias de pacientes.
* Opciones Adicionales (Mayor Complejidad)
* Recordatorios automáticos de turnos (mail o notificación).
# 🏗️ Estructura del proyecto
* **Backend (`/backend`)**: Construido con Python y FastApi, se desarrollo un API encargada de toda la gestion de la logica del negocio. 

* **Frontend (`/frontend`)**: Contruido en React con TypeScript, ademas de utilizar bootstrap para un mejor diseño.

# 📖 Aprendiendo sobre la marcha
Al principio estuvimos viendo que tecnologias utilizar, ya que la mayoria del grupo no habia trabajado con python para hacer una aplicacion tan compleja. Luego de un par de dias de investigacion dimos con **Fast Api**, que nos parecio la mejor idea para hacer un backend ya que la mayoria de nosotros habia trabajado con APIs anteriormente.

Luego tuvimos que ver que patron o principios implementar. Comentamos con nuestros compañeros que no habia una biblioteca o tecnologia que pudieramos entender para realizar la persistencia de datos, entonces recordamos la inversion de dependencias. Si bien esto iba a ser un poco mas engorroso, ya que tendriamos que crear clases de implementacion para cada una de las clases que necesitaramos persistir, pensamos que seria divertido y nos ayudaria a entender un poco mas como funcionaria el acceso a la base de datos y como de deben de guardar esa informacion.