# dependencias
from flask import render_template, session, request, redirect, url_for, send_file, send_from_directory
from modules.config import app #importamos la instancia de Flask
from modules.funcionalidades import (listar_peliculas, cargar_datos_peliculas, 
                                     generar_frases_aleatorias, generar_intentos, 
                                     leer_archivo_resultados_historicos, 
                                     mostrar_resultados_formateados, 
                                     guardar_resultado_partida,
                                     generar_graficos, generar_pdf)
import datetime

app.secret_key = 'clave_secreta' #clave para la sesión
ruta = "./data/"
ruta_archivo_resultados = ruta + "resultados_partidas.txt"

@app.route('/', methods=['GET', 'POST'])
def p_inicio():
    if request.method == 'POST': #si se envía el formulario
        nombre_usuario = request.form.get("username") 
        n_frases = request.form.get("nfrases")

        if not nombre_usuario or not n_frases:
            return redirect(url_for("p_inicio"))
        
        try:
            n_frases = int(n_frases) #convertimos a entero
            if n_frases < 3 or n_frases > 10:  # cantidad de frases entre 3 y 10
                return redirect(url_for("p_inicio"))
        except ValueError:
            return redirect(url_for("p_inicio"))
        
        session['usuario'] = nombre_usuario
        session['n_frases'] = n_frases
        session['puntaje'] = 0  #inicializar puntaje

        return redirect(url_for("p_iniciar_trivia"))

    return render_template('inicio.html')

@app.route('/trivia', methods=['GET', 'POST'])
def p_iniciar_trivia():
    if request.method == 'POST':
        accion = request.form.get('accion')

        if accion == 'responder' and session['estado'] == 'siguiente':   #usuario respondió la pregunta actual
            respuesta = request.form.get('respuesta')
            session['seleccion'] = respuesta  

            indice = session.get('indice', 0)
            pregunta_actual = session['trivia'][indice]

            # verifico la respuesta
            if respuesta == pregunta_actual['correcta']:
                session['puntaje'] += 1
                session['mensaje'] = "¡Correcto!"
            else:
                session['mensaje'] = f"Incorrecto. La respuesta correcta es: {pregunta_actual['correcta']}."

            session['estado'] = 'evaluando' #cambio el estado a evaluando para que no pueda responder nuevamente

        elif accion == 'siguiente' and session['estado'] == 'evaluando':   #siguiente pregunta
            session['indice'] += 1 #incremento el índice para la siguiente pregunta
            session['estado'] = 'siguiente' #cambio el estado a siguiente para que pueda responder nuevamente
            session['mensaje'] = None #limpio el mensaje de la pregunta anterior
            session['seleccion'] = None #limpio la selección del usuario

            if session['indice'] >= len(session['trivia']): #si ya no hay más preguntas
                session['puntaje_final'] = session['puntaje'] 
                return redirect(url_for('p_resultado_trivia')) 

    else:
        #cada vez que se inicia una nueva trivia, se actualiza la fecha
        session['fecha_hora_inicio'] = datetime.datetime.now().strftime("%d-%m-%y %H:%M")

        #cargar preguntas (nuevas)
        datos_peliculas = cargar_datos_peliculas("data/frases_de_peliculas.txt")
        frases_aleatorias = generar_frases_aleatorias(datos_peliculas, session['n_frases'])
        intentos = generar_intentos(frases_aleatorias, datos_peliculas)

        session['trivia'] = intentos
        session['indice'] = 0  #nro de pregunta/frase actual
        session['puntaje'] = 0
        session['mensaje'] = None  
        session['estado'] = 'siguiente'
        session['seleccion'] = None  

    indice = session.get('indice', 0) #obtengo el índice de la pregunta actual, 0 si no existe
    pregunta_actual = session['trivia'][indice] #obtengo la pregunta actual

    return render_template('trivia.html',  
                           pregunta=pregunta_actual, 
                           usuario=session['usuario'], 
                           total_preguntas=session['n_frases'], 
                           indice=indice, 
                           mensaje=session.get('mensaje', None),  
                           estado=session['estado'],
                           seleccion=session.get('seleccion', None))


@app.route('/resultados')
def p_resultado_trivia():
    puntaje = session.get('puntaje_final', 0)
    usuario = session.get('usuario', 'Invitado')
    intentos = session.get('n_frases', 0)

    guardar_resultado_partida(session['usuario'], session['n_frases'], session['puntaje_final'], 
                               session['fecha_hora_inicio'], ruta_archivo_resultados)

    #limpiar la sesión para la siguiente trivia
    session.pop('trivia', None)
    session.pop('indice', None)
    session.pop('puntaje', None)
    session.pop('mensaje', None)
    session.pop('estado', None)
    session.pop('puntaje_final', None)

    return render_template(
        'resultados.html', 
        puntaje=puntaje, 
        intentos=intentos, 
        usuario=usuario
    )


@app.route('/listado-peliculas')
def p_listado_peliculas():
    lista_peliculas = listar_peliculas("data/frases_de_peliculas.txt")
    return render_template('listado_peliculas.html', peliculas=lista_peliculas)

@app.route('/resultados_historicos')
def p_resultados_historicos():
    resultados = leer_archivo_resultados_historicos(ruta_archivo_resultados)
    resultados_tabla = mostrar_resultados_formateados(resultados)
    return render_template('resultados_historicos.html', p_tabla=resultados_tabla)

#redirecciona a la carpeta data para mostrar imagenes
@app.route('/data/<path:filename>')
def mostrar_imagen_data(filename):
    return send_from_directory('data', filename)

@app.route('/resultados_graficos')
def p_resultados_graficos():
    generar_graficos() 
    return render_template("resultados_graficos.html")


@app.route("/descargar_pdf")
def descargar_pdf():
    try:
        pdf_path = generar_pdf() #generamos el PDF y obtenemos la ruta
        return send_file(pdf_path, as_attachment=True, download_name="resultados.pdf", mimetype="application/pdf")
    except Exception as e:
        return f"Error al generar el PDF: {str(e)}", 500  # Manejo de errores

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
