# ⚙️  Backend Sistema Gestion de Turnos para Medicos
Este es el API que permite la gestion de la logica de negocio del sistema. 

En este proyecto necesitabamos aplicar un patron de diseño, y en grupo decidimos aplicar inversion de dependecias con una interfaz de persistencia. Esta nos permite tener varios repositorios que utilizen esa interfaz pero que la implementacion de estos puede ser distinta para distintas base de datos.
### Base de datos
Utilizamos Sqlite como base de datos ya que nos permite crear un archivo *.db* el cual es facil de manejar y ver su contenido ademas poder modificar su estructura con varias herramientas de base de datos.

# 🗂️ Estructura de Carpetas
* 📁 **`/controllers`**: Esta carpeta contiene la logica de los distitos controladores que llevan a cabo la logica de cada uno de los casos de uso.
* 📁 **`/interfaces`**: Esta carpeta tiene la interface de persistecia de las cuales los distintos repositorios van a necesitar implementar.
* 📁 **`models`**: Esta carpeta contiene las distintas clases de negocio.
* 📁 **`/pdfs`**: Aqui se generan los distintos reportes y estadisticas.
* 📁 **`/repositories`**: En esta carpeta se encuentran las implementaciones para la persistencia de los objetos del dominio.
* 📁 **`/routes`**: Aqui se encuentran los endpoitns del API, donde cada uno de estos endpoits utilizan el controller para responder a la peticion que se recibio.
* 📁 **`/schemas`**: Son clases que se van a utilizar para la persistencia en la DB.

# 🛠️ Dependencias
En el proyecto estamos utilizando fastAPI ademas de uvicorn. Para instalar estas dependencias utilizamos el siguiente comando:

`$ python -m pip install fastapi uvicorn`

# ✅ Iniciar el proyecto

`$ python -m uvicorn app:app --reload`