#dependencias
from flask import render_template, session, request, redirect, url_for
from modules.config import app
from modules.funcionalidades import guardar_nombre_usuario, listar_peliculas, cargar_datos_peliculas, cargar_datos_usuario, generar_frases_aleatorias, generar_intentos
from modules.info_usuario import guardar_usuario_en_archivo, agregar_usuario_nfrases, cargar_lista
from random import sample
import random
app.secret_key = 'clave_secreta'

ruta = "./data/"
ruta_archivo = ruta + "datos_usuario.txt"

lista_usuarios = [] #lista auxiliar
lista_temporal_usuario = []

# try:
#     cargar_lista(ruta_archivo, lista_usuarios)            
# except FileNotFoundError:
#     with open(ruta_archivo, "w") as archi:
#         pass

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
        
        lista_temporal_usuario.append(nombre_usuario)
        lista_temporal_usuario.append(n_frases)
        print(lista_temporal_usuario)

        return redirect(url_for("p_iniciar_trivia"))

    return render_template('inicio.html')


@app.route('/trivia', methods=['GET', 'POST'])
def p_iniciar_trivia():
    if request.method == 'POST':
        # Procesar la respuesta del usuario
        respuesta = request.form.get('respuesta')
        indice = session.get('indice', 0)
        pregunta_actual = session['trivia'][indice]

        # Verificar si la respuesta es correcta
        if respuesta == pregunta_actual['correcta']:
            session['puntaje'] += 1

        # Avanzar al siguiente índice
        session['indice'] += 1

        # Si ya no hay más preguntas, redirigir a la página de resultados
        if session['indice'] >= len(session['trivia']):
            return redirect(url_for('resultado_trivia'))
    else:

        datos_peliculas = cargar_datos_peliculas("data/frases_de_peliculas.txt")
        frases_aleatorias = generar_frases_aleatorias(datos_peliculas, lista_temporal_usuario[1]) #n_frases
        intentos = generar_intentos(frases_aleatorias, datos_peliculas)

        session['trivia'] = intentos
        session['indice'] = 0 #control de los intentos
        session['puntaje'] = 0
        session['usuario'] = lista_temporal_usuario[0] #nombre de usuario
        session['n_frases'] = lista_temporal_usuario[1]

    indice = session.get('indice', 0)
    pregunta_actual = session['trivia'][indice]
    return render_template('trivia.html', pregunta = pregunta_actual)

@app.route('/resultado')
def resultado_trivia():
    puntaje = session.get('puntaje', 0)
    session.pop('trivia', None)
    session.pop('indice', None)
    session.pop('puntaje', None)
    return f"Tu puntuación final es: {puntaje}"


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