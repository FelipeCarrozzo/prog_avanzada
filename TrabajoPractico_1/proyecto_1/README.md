# 🐍Trivia de Películas

Al comenzar, el usuario elige cuántas frases quiere adivinar. Luego, se le presentan frases famosas y debe seleccionar la película correcta entre tres opciones. El sistema da retroalimentación inmediata y, al finalizar, muestra el puntaje obtenido, un resumen de resultados históricos y gráficos de desempeño. Además, se puede generar un PDF con los gráficos estadísticos.


---
## 🏗Arquitectura General

EL código está organizado en un archivo principal **server.py**, que integra todas las funcionalidades y define las rutas de la aplicación usando Flask, administrando la lógica del juego. 
Luego está el archivo **funcionalidades.py**, que define las funciones que realizan tareas específicas. 
Por último, en el módulo *templates* se encuentran los archivos **.html**, para cada parte del juego. 
---
## 📑Dependencias

1. **Python 3.12.4**
2. **Flask**
3. **fpdf**
4. **matplotlib**
5. **pandas**

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

**Ejemplo**:
- **Inicio** (`/`): muestra la página de inicio.
- **Listado películas** (`/listado-peliculas`): lista todas las películas entre las que elegirás. 
- **Trivia** (`/trivia`): muestra la página del juego.
- **Resultados** (`/resultados`): mmuestra los resultados del usuario luego de jugar
- **Resultados históricos** (`/resultados_historicos`): muestra los resultados de todas las partidas ordenadas por fecha. 
- **Resultados gráficos** (`/resultados_graficos`): muestra gráficamente los resultados. 


---

## 🙎‍♀️🙎‍♂️Autores

- Caporizzo Agustina
- Carrozzo Felipe
---

