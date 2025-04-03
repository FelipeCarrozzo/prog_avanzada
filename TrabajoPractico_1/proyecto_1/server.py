# dependencias
from flask import render_template, session, request, redirect, url_for, send_file
from modules.config import app
from modules.funcionalidades import (listar_peliculas, cargar_datos_peliculas, 
                                     generar_frases_aleatorias, generar_intentos, 
                                     leer_archivo_resultados_historicos, 
                                     mostrar_resultados_formateados, 
                                     guardar_usuario_en_archivo,
                                     generar_graficos, generar_pdf)  # Asegúrate de importar generar_pdf
import datetime

app.secret_key = 'clave_secreta'
ruta = "./data/"
ruta_archivo_datos_usuario = ruta + "datos_usuario.txt"

@app.route('/', methods=['GET', 'POST'])
def p_inicio():
    if request.method == 'POST':
        nombre_usuario = request.form.get("username")
        n_frases = request.form.get("nfrases")

        if not nombre_usuario or not n_frases:
            return redirect(url_for("p_inicio"))
        
        try:
            n_frases = int(n_frases)
            if n_frases < 1 or n_frases > 10:  # Validar rango de frases
                return redirect(url_for("p_inicio"))
        except ValueError:
            return redirect(url_for("p_inicio"))
        
        session['usuario'] = nombre_usuario
        session['n_frases'] = n_frases
        session['puntaje'] = 0  # Inicializar puntaje

        return redirect(url_for("p_iniciar_trivia"))

    return render_template('inicio.html')

@app.route('/trivia', methods=['GET', 'POST'])
def p_iniciar_trivia():
    if request.method == 'POST':
        accion = request.form.get('accion')

        if accion == 'responder' and session['estado'] == 'siguiente':  
            # Usuario responde la pregunta
            respuesta = request.form.get('respuesta')
            session['seleccion'] = respuesta  

            indice = session.get('indice', 0)
            pregunta_actual = session['trivia'][indice]

            # Verificamos la respuesta
            if respuesta == pregunta_actual['correcta']:
                session['puntaje'] += 1
                session['mensaje'] = "¡Correcto!"
            else:
                session['mensaje'] = f"Incorrecto. La respuesta correcta es: {pregunta_actual['correcta']}."

            session['estado'] = 'evaluando'  

        elif accion == 'siguiente' and session['estado'] == 'evaluando':
            # Avanzamos a la siguiente pregunta
            session['indice'] += 1
            session['estado'] = 'siguiente'  
            session['mensaje'] = None  
            session['seleccion'] = None  

            if session['indice'] >= len(session['trivia']):
                session['puntaje_final'] = session['puntaje']
                return redirect(url_for('p_resultado_trivia'))

    else:
        # **Cada vez que se inicia una nueva trivia, se actualiza la fecha**
        session['fecha_hora_inicio'] = datetime.datetime.now().strftime("%d-%m-%y %H:%M")

        # Cargar nuevas preguntas
        datos_peliculas = cargar_datos_peliculas("data/frases_de_peliculas.txt")
        frases_aleatorias = generar_frases_aleatorias(datos_peliculas, session['n_frases'])
        intentos = generar_intentos(frases_aleatorias, datos_peliculas)

        session['trivia'] = intentos
        session['indice'] = 0
        session['puntaje'] = 0
        session['mensaje'] = None  
        session['estado'] = 'siguiente'
        session['seleccion'] = None  

    indice = session.get('indice', 0)
    pregunta_actual = session['trivia'][indice]

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

    guardar_usuario_en_archivo(session['usuario'], session['n_frases'], session['puntaje_final'], 
                               session['fecha_hora_inicio'], ruta_archivo_datos_usuario)

    # Limpiar la sesión para la siguiente trivia
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
    resultados = leer_archivo_resultados_historicos(ruta_archivo_datos_usuario)
    resultados_tabla = mostrar_resultados_formateados(resultados)
    return render_template('resultados_historicos.html', p_tabla=resultados_tabla)

@app.route('/resultados_graficos')
def p_resultados_graficos():
    generar_graficos()  # Genera los gráficos antes de mostrar la página
    return render_template("resultados_graficos.html")


@app.route("/descargar_pdf")
def descargar_pdf():
    try:
        pdf_path = generar_pdf()  # Llamada a la función que genera el PDF
        return send_file(pdf_path, as_attachment=True, download_name="resultados.pdf", mimetype="application/pdf")
    except Exception as e:
        return f"Error al generar el PDF: {str(e)}", 500  # Manejo de errores

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
