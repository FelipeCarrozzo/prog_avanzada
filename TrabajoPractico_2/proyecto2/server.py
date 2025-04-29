# Ejemplo de aplicación principal en Flask
from flask import render_template, session, request, redirect, url_for, send_file, send_from_directory
from modules.config import app
from modules.cinta import Cinta
from modules.detector import DetectorAlimento
from modules.cajon import Cajon
from modules.calculador import CalculadorBromatologico
from modules.alimentos import Alimentos, Verdura, Fruta, Kiwi, Manzana, Papa, Zanahoria


# Página de inicio
@app.route('/', methods=['GET', 'POST'])
def index():
    alimentos = [] #borrar antes de entregar
    detector = DetectorAlimento()
    cajon = Cajon()
    calculador = CalculadorBromatologico()
    cinta = Cinta(detector, cajon)
    if request.method == 'POST':
        #genero objetos
        n_alimentos = int(request.form.get("n_alimentos"))  #viene desde html
        if n_alimentos:
            print("se detectó el número de alimentos")
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

    calculos_aw_promedio = {
    "aw_kiwi": calculador.calcular_aw(Kiwi,cajon),
    "aw_manzana": calculador.calcular_aw(Manzana,cajon),
    "aw_papa": calculador.calcular_aw(Papa,cajon),
    "aw_zanahoria": calculador.calcular_aw(Zanahoria,cajon),
    "aw_frutas": calculador.calcular_aw(Fruta,cajon),
    "aw_verduras": calculador.calcular_aw(Verdura,cajon),
    "aw_total": calculador.calcular_aw(Alimentos,cajon)
    }

    print("Valores de aw promedio:", calculos_aw_promedio)

    

    return render_template('index.html', lista_alimentos=alimentos, n_alimentos=session.get("n_alimentos"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)