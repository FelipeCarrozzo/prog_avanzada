# 🐍Cinta Transportadora de alimentos

Este es un proyecto implementado con el framework [Flask](https://flask.palletsprojects.com/). Aquí se implementa una cinta transportadora de alimentos, la cual agrega al cajón la cantidad que el usuario desee. Esta cinta tiene la capacidad de pesar el cajón de alimentos una vez que 
fueron agregados. También se calcula la actividad acuosa promedio de los alimentos, para advertir al usuario si son aptos para el consumo o no. 

---
## 🏗Arquitectura General

El proyecto está construido con una arquitectura orientada a objetos y utiliza Flask como servidor web para coordinar la interacción entre los distintos módulos. El archivo server.py funciona como punto de entrada y orquestador del sistema, exponiendo endpoints que integran los componentes principales: el Detector, la Cinta, el CalculadorBromatologico y el Cajon. Cada uno de estos está encapsulado en su propia clase, representando entidades del dominio. La clase Cinta cumple el rol de procesar los alimentos detectados y derivarlos a los cajones correspondientes según su clasificación. Los alimentos (Kiwi, Manzana, Papa, Zanahoria) están modelados como clases especializadas, heredando de una base común, lo que permite aplicar polimorfismo. Esta estructura modular y orientada a objetos favorece la mantenibilidad y facilita futuras extensiones del sistema.

El diagrama de relaciones UML está disponible en la carpeta [docs](./docs) del proyecto.

---
## 📑Dependencias

1. **Python 3.x**
2. **Flask** (`pip install flask`)
5. Dependencias listadas en requierements.txt

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

Para usar la aplicación, se debe ejecutar el archivo [server.py]. 

**Ejemplo**:
- **Ruta principal** (`/`): muestra la página de inicio.
- **Ruta de usuario** (`/user/<id>`): muestra información del usuario.

---

## 🙎‍♀️🙎‍♂️Autores

- Caporizzo Agustina
- Carrozzo Felipe
