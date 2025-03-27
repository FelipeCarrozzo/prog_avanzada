#dependencias
from flask import render_template, session, request, redirect, url_for
from modules.config import app
from modules.funcionalidades import guardar_nombre_usuario, listar_peliculas, cargar_datos_peliculas, cargar_datos_usuario
from modules.info_usuario import guardar_usuario_en_archivo, agregar_usuario_nfrases, cargar_lista
from random import sample
import random

ruta = "./data/"
ruta_archivo = ruta + "datos_usuario.txt"

lista_usuarios = [] #lista auxiliar

try:
    cargar_lista(ruta_archivo, lista_usuarios)            
except FileNotFoundError:
    with open(ruta_archivo, "w") as archi:
        pass

@app.route('/', methods=['GET', 'POST'])
def p_inicio():
    if request.method == 'POST':
        print("Formulario recibido")  # Ver si entra en el bloque

        nombre_usuario = request.form.get("username")
        n_frases = request.form.get("nfrases")

        if not nombre_usuario or not n_frases:
            print("Error: Datos incompletos")
            return redirect(url_for("p_inicio"))

        try:
            n_frases = int(n_frases)
        except ValueError:
            print("Error: n_frases no es un número")
            return redirect(url_for("p_inicio"))

        print(f"Guardando usuario: {nombre_usuario}, {n_frases}")

        guardar_usuario_en_archivo(ruta_archivo, nombre_usuario, n_frases)

        return redirect(url_for("p_iniciar_trivia"))

    return render_template('inicio.html')


#pagina del juego
@app.route('/trivia')
def p_iniciar_trivia():
    #leer nombe de usuario y cant de frases
    nusuario, nfrases = cargar_datos_usuario(ruta_archivo)
    #se debe leer el archivo de peliculas y frases

    datos_peliculas = cargar_datos_peliculas("data/frases_de_peliculas.txt")
    frases_pelis_aleatorias = sample(list(datos_peliculas.items()), nfrases)
    print(frases_pelis_aleatorias)
    trivia = []
    peliculas_totales = list(datos_peliculas.values())
    
    for frase, pelicula_correcta in frases_pelis_aleatorias:
        opciones = [pelicula_correcta]
    
        peliculas_incorrectas = list(set(peliculas_totales) - {pelicula_correcta})
        opciones += sample(peliculas_incorrectas, 2) #agrego dos incorrectas

        random.shuffle(opciones)

        trivia.append({'frase': frase, 'opciones': opciones, 'correcta': pelicula_correcta})
        
    return render_template('trivia.html', trivia = trivia)


#pagina de listado de películas
@app.route('/listado-peliculas')
def p_listado_peliculas():
    lista_peliculas = listar_peliculas("data/frases_de_peliculas.txt")
    return render_template('listado_peliculas.html', peliculas = lista_peliculas)

#pagina de resultados
@app.route('/resultados-historicos')
def p_resultados_historicos():
    return render_template('resultados.html')

@app.route('/resultados-graficos')
def p_resultados_graficos():
    return render_template('graficos.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)