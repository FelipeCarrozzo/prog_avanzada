# 🐍Sistema de Información Universitaria

Este es un proyecto en Python que simula un sistema de gestión universitaria. Permite registrar estudiantes y profesores, crear facultades, departamentos y cursos, e inscribir estudiantes en dichos cursos. Se ejecuta desde consola y se organiza utilizando programación orientada a objetos.

---

## 🏗Arquitectura General

El sistema está compuesto por las siguientes entidades principales implementadas como clases:

- `Persona` (abstracta): clase base para `Estudiante` y `Profesor`.
- `Estudiante`: representa a un estudiante con nombre, apellido y DNI.
- `Profesor`: representa a un docente con sus datos personales.
- `Curso`: incluye nombre y un profesor responsable.
- `Departamento`: agrupa cursos bajo la coordinación de un profesor.
- `Facultad`: agrupa departamentos, profesores y estudiantes.

El flujo principal de la aplicación se gestiona desde el archivo `main.py`.

El diagrama de relaciones entre clases está disponible en la carpeta [docs](./docs) del proyecto.

---

## 📑Dependencias

Este proyecto tiene muy pocas dependencias externas. Las principales son:

1. **Python 3.x**
2. Solo se utilizan módulos estándar (`os`, etc.)

Si se agregan más funcionalidades, las dependencias se listarán en el archivo `requirements.txt` ubicado en la carpeta [deps](./deps).

---
## 🚀Cómo Ejecutar el Proyecto
1. **Clonar o descargar** el repositorio.

2. **(Opcional)** Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/macOS
   .\venv\Scripts\activate   # En Windows
---

## 💻Uso de la aplicación

Al ejecutar el archivo `main.py`, el usuario interactúa con el sistema a través de un menú en consola que le permite gestionar distintos aspectos de la universidad. No se requieren credenciales ni autenticación.

### Menú de opciones:
##########################################
Sistema de Información Universitaria
##########################################
Elige una opción
1 - Inscribir estudiante
2 - Contratar profesor
3 - Crear departamento nuevo
4 - Crear curso nuevo
5 - Inscribir estudiante a un curso
6 - Salir

### Funcionalidades principales:

- **Inscribir estudiante**: permite ingresar los datos de un nuevo estudiante y asignarlo a una facultad.
- **Contratar profesor**: registra un nuevo profesor en la facultad seleccionada.
- **Crear departamento nuevo**: se asigna un director entre los profesores existentes.
- **Crear curso nuevo**: dentro de un departamento existente, con profesor titular.
- **Inscribir estudiante a un curso**: seleccionando estudiante y curso disponibles.
- **Salir**: finaliza la ejecución del sistema.

El sistema inicializa automáticamente una facultad leyendo hasta 4 estudiantes y 4 profesores desde el archivo `data/personas.txt`.

---

## 🙎‍♀️🙎‍♂️Autores

- Caporizzo Agustina
- Carrozzo Felipe

---

> **Consejo**: Mantén el README **actualizado** conforme evoluciona el proyecto, y elimina (o añade) secciones según necesites. Esta plantilla es sólo un punto de partida general.
