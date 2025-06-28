# 🐍Gestor de reclamos para la Facultad De Ingeniería 

Breve descripción del proyecto:
Esta es una aplicación web construida con el framework [Flask](https://flask.palletsprojects.com/). Permite a los estudiantes, docentes y PAyS de la facultad generar reclamos sobre posibles faltantes, fallas o desperfectos que existan en las áreas comunes del edificio. Los usuarios pueden hacer un seguimiento del estado de su reclamo. 

---
## 🏗Arquitectura General

El proyecto está organizado en módulos siguiendo una arquitectura por capas:
- **Capa de dominio:** Clases principales como `Reclamo` y `Usuario`.
- **Capa de servicios:** Clases gestoras como `GestorReclamos`, `GestorReportes`, `GestorExportacion`.
- **Capa de persistencia:** Repositorios abstractos y concretos para acceso a base de datos.
- **Capa de presentación:** Vistas y rutas Flask.
- **Utilidades:** Módulos auxiliares para clasificación, estadísticas, gráficos, etc.

El diagrama de relaciones entre clases está disponible en la carpeta [docs](./docs) del proyecto.


---
## 📑Dependencias

1. **Python 3.x**
2. **Flask** (`pip install flask`)
3. **SQLAlchemy** (`pip install sqlalchemy`)
4. **nltk**, **numpy**, **scikit-learn**, **matplotlib**, **wordcloud**, **reportlab**, **pytest**, **flask-login**, **flask-session**, **flask-wtf**, **flask-bootstrap**, **WTForms**, **email-validator**, **scipy**, **Werkzeug**
5. Todas las dependencias están listadas en `requirements.txt` (en la carpeta [deps](./deps)).


---
## 🚀Cómo Ejecutar el Proyecto
1. **Clonar o descargar** el repositorio.

2. **Crear y activar** un entorno virtual.

3. **Instalar las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
   El archivo `requirements.txt` se encuentran en la carpeta [deps](./deps) del proyecto.
   
---

## 💻Uso de la aplicación

- **Ruta principal** (`/`): Página de inicio y acceso.
- **/login**: Formulario de inicio de sesión.
- **/register**: Registro de nuevos usuarios.
- **/reclamos**: Listado y creación de reclamos.
- **/reclamo/<id>**: Detalle de un reclamo.
- **/reportes**: Visualización y exportación de reportes.
- **/logout**: Cierre de sesión.


**Autenticación:**  
Para acceder a la mayoría de las funcionalidades es necesario estar registrado e iniciar sesión. El flujo típico es:
1. Registro de usuario.
2. Login.
3. Acceso a la gestión de reclamos y reportes.

---

## 🙎‍♀️🙎‍♂️Autores

- Carrozzo Felipe
- Caporizzo Agustina
---
