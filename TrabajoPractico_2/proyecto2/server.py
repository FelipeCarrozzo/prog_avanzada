# Ejemplo de aplicación principal en Flask
from flask import render_template, session, request, redirect, url_for, send_file, send_from_directory
from modules.config import app
from modules.cinta import Cinta
from modules.detector import DetectorAlimento
from modules.cajon import Cajon

app.secret_key = "trabajo2_PA"

# Página de inicio
@app.route('/', methods=['GET', 'POST'])
def index():
    alimentos = []
    if request.method == 'POST':
        
        #genero objetos
        n_alimentos = int(request.form.get("n_alimentos"))  #viene desde html
        if n_alimentos:
            print("se detectó el número de alimentos")
            # session['n_alimentos'] = int(n_alimentos)  #convierte a entero
            detector = DetectorAlimento()
            cajon = Cajon(n_alimentos)
            cinta = Cinta(detector, cajon)

            contador = 0
            while contador < n_alimentos:
                print("Alimento en la cinta: ")
                alimento = cinta.clasificar_alimentos()
                if alimento is not None:
                    cajon.agregar_alimento(alimento)
                    alimentos.append(alimento)
                    contador += 1
                else:
                    print("Alimento inválido")
            
        print("Alimentos en la sesión:", cajon.mostrar_contenido_cajon())
    

    return render_template('index.html', lista_alimentos=alimentos, n_alimentos=session.get("n_alimentos"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)