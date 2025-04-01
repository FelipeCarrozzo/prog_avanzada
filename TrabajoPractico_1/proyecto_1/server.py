#dependencias
from flask import render_template, session, request, redirect, url_for
from modules.config import app
from modules.funcionalidades import listar_peliculas, cargar_datos_peliculas, generar_frases_aleatorias, generar_intentos, leer_archivo_resultados_historicos, mostrar_resultados_formateados, guardar_usuario_en_archivo
from random import sample
import datetime
app.secret_key = 'clave_secreta'

ruta = "./data/"
ruta_archivo_datos_usuario = ruta + "datos_usuario.txt"

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
            if n_frases < 1 or n_frases > 10: #si es menor a 1 o mayor a 10
                print("Error: n_frases fuera de rango")
                return redirect(url_for("p_inicio"))
        except ValueError:
            print("Error: n_frases no es un número")
            return redirect(url_for("p_inicio"))
        
        session['usuario'] = nombre_usuario
        session['n_frases'] = n_frases

        return redirect(url_for("p_iniciar_trivia"))

    return render_template('inicio.html')


@app.route('/trivia', methods=['GET', 'POST'])
def p_iniciar_trivia():
    fecha_hora_inicio = datetime.datetime.now()
    fecha_hora_inicio = fecha_hora_inicio.strftime("%Y-%m-%d %H:%M:%S")
    if request.method == 'POST':
        # Procesar la respuesta del usuario
        respuesta = request.form.get('respuesta')
        indice = session.get('indice', 0)
        pregunta_actual = session['trivia'][indice]

        # Verificar si la respuesta es correcta
        if respuesta == pregunta_actual['correcta']:
            session['puntaje'] += 1
            session['mensaje'] = "¡Correcto!"
        # Avanzar al siguiente índice
        session['indice'] += 1
        # Si ya no hay más preguntas, redirigir a la página de resultados
        if session['indice'] >= len(session['trivia']):
            session['puntaje_final'] = session['puntaje']
            session['fecha_hora_inicio'] = fecha_hora_inicio
            guardar_usuario_en_archivo(session['usuario'],session['n_frases'], session['puntaje_final'], 
                                       session['fecha_hora_inicio'], ruta_archivo_datos_usuario)
            return redirect(url_for('p_resultado_trivia'))
    else:

        datos_peliculas = cargar_datos_peliculas("data/frases_de_peliculas.txt")
        frases_aleatorias = generar_frases_aleatorias(datos_peliculas, session['n_frases']) #n_frases
        intentos = generar_intentos(frases_aleatorias, datos_peliculas)
        print(intentos)
        session['trivia'] = intentos
        session['indice'] = 0 #control de los intentos
        session['puntaje'] = 0

    indice = session.get('indice', 0)
    pregunta_actual = session['trivia'][indice]
    return render_template('trivia.html', pregunta = pregunta_actual, usuario = session['usuario'], intentos = session['n_frases'],
                           mensaje = session.get('mensaje', None))

@app.route('/resultados')
def p_resultado_trivia():
    intentos = session.get('trivia', [])
    if not intentos:
        return redirect(url_for('p_inicio')) #para que intentos siempre tenga un valor
    puntaje = session.get('puntaje', 0)
    session.pop('trivia', None) 
    session.pop('indice', None)
    session.pop('puntaje', None)
    return render_template('resultados.html', puntaje = puntaje, intentos = session['n_frases'], 
                           usuario = session['usuario'])

@app.route('/resultados_historicos')
def p_resultados_historicos():
    # Cargar los datos de los usuarios desde el archivo
        resultados = leer_archivo_resultados_historicos(ruta_archivo_datos_usuario)
        resultados_tabla = mostrar_resultados_formateados(resultados) #imprime en consola los resultados

        return render_template('resultados_historicos.html', p_tabla = resultados_tabla)


#pagina de listado de películas
@app.route('/listado-peliculas')
def p_listado_peliculas():
    lista_peliculas = listar_peliculas("data/frases_de_peliculas.txt")
    return render_template('listado_peliculas.html', peliculas = lista_peliculas)


@app.route('/resultados-graficos')
def p_resultados_graficos():
    return render_template('graficos.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)