# Ejemplo de aplicación principal en Flask
# dependencias
from flask import render_template, request, redirect, url_for
from modules.config import app
from modules.funciones import agregar_libro_a_lista, cargar_lista_desde_archivo, guardar_libro_en_archivo

RUTA = "./data/"
ARCHIVO = RUTA + "libros_leidos.txt"

lista_libros = [] #lista auxiliar

try:
    cargar_lista_desde_archivo(ARCHIVO, lista_libros)            
except FileNotFoundError:
    with open(ARCHIVO, "w") as archi:
        pass


# Página de inicio
@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/listar')
def funcion_listar():
    if len(lista_libros) == 0:
        return render_template("listar.html", mi_lista = lista_libros, vacio = True)
    return render_template('listar.html', mi_lista=lista_libros)

@app.route('/agregar', methods = ['GET', 'POST'])
def funcion_agregar():
    if request.method == "POST":
        # Procesamos los datos del formulario
        nombre = request.form["input_nombre"]
        autor = request.form["input_autor"]
        calificacion = request.form["input_calif"]
        # Guardamos los datos en el archivo
        guardar_libro_en_archivo(ARCHIVO, nombre, autor, calificacion)
        # Agregamos el libro a la lista
        agregar_libro_a_lista(lista_libros, nombre, autor, calificacion)
        # Redirigimos a la página de inicio
        return redirect(url_for("inicio"))
    
    return render_template("agregar.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)