# Ejemplo de aplicación principal en Flask
from flask import render_template, session, request, redirect, url_for, send_file, send_from_directory
from modules.config import app
from modules.cinta import Cinta
from modules.detector import DetectorAlimento
from modules.cajon import Cajon

# Página de inicio
@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        #genero objetos
        n_alimentos = request.form.get("n_alimentos") #viene desde html
        if n_alimentos:
            # session['n_alimentos'] = int(n_alimentos) #convierte a enter
            session['n_alimentos'] = 10
            detector = DetectorAlimento()
            cajon = Cajon(n_alimentos)
            cinta = Cinta(detector, cajon)

            alimentos = []
            for i in range(session['n_alimentos']):
                print("Alimento en la cinta: ", i)
                alimento = cinta.clasificar_alimentos()
                if alimento:
                    cajon.agregar_alimento(alimento)
                    alimentos.append(alimento)
                    # session['alimentos'] = [alimento] #almacena el alimento en la sesion
        print("Alimentos en la sesión:", alimentos)
            
    # return (alimentos)


    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)