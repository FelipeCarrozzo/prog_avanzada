from flask import render_template, request
from modules.config import app
from modules.cinta import Cinta
from modules.detector import DetectorAlimento
from modules.cajon import Cajon
from modules.calculador import CalculadorBromatologico
from modules.alimentos import Alimentos, Verdura, Fruta, Kiwi, Manzana, Papa, Zanahoria

# Página de inicio
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Función que maneja la página de inicio de la aplicación.
    Permite al usuario clasificar alimentos y calcular su actividad acuosa.
    """
    #genero objetos
    detector = DetectorAlimento()
    cajon = Cajon()
    calculador = CalculadorBromatologico()
    cinta = Cinta(detector, cajon)

    #creo un diccionario para guardar los valores de aw promedio
    calculos_aw_promedio = {
        "aw_kiwi": 0.0,
        "aw_manzana": 0.0,
        "aw_papa": 0.0,
        "aw_zanahoria": 0.0,
        "aw_frutas": 0.0,
        "aw_verduras": 0.0,
    }

    peso_total = 0.0
    revisar = False 

    #verifico si el formulario fue enviado por el usuario
    if request.method == 'POST':
        n_alimentos = int(request.form.get("n_alimentos"))  #viene desde html
        if n_alimentos:

            #verifico la cantidad de alimentos a clasificar
            contador = 0
            while contador < n_alimentos:
                alimento = cinta.clasificar_alimentos()

                #mientras el alimento no sea None, lo agrego al cajon
                if alimento is not None:
                    cajon.agregar_alimento(alimento)
                    contador += 1
                else:
                    print("Alimento inválido")

    #genero los calculos de aw para cada alimento. Si el alimento no se encuentra en el cajón,
    #el valor es 0
    calculos_aw_promedio = {
    "aw_kiwi": round(calculador.calcular_aw(Kiwi,cajon),2),
    "aw_manzana": round(calculador.calcular_aw(Manzana,cajon),2),
    "aw_papa": round(calculador.calcular_aw(Papa,cajon),2),
    "aw_zanahoria": round(calculador.calcular_aw(Zanahoria,cajon),2),
    "aw_frutas": round(calculador.calcular_aw(Fruta,cajon),2),
    "aw_verduras": round(calculador.calcular_aw(Verdura,cajon),2),
    "aw_total": round(calculador.calcular_aw(Alimentos,cajon),2)
    }

    #calculo peso del cajon con la funcion de la clase Cajon
    peso_total = round(cajon.calcular_peso(),2)

    #verifico que el valor de aw promedio no sea mayor a 1 o menor a 0
    for valor in calculos_aw_promedio.values():
        if valor > 0.90:
            revisar = True
            break

    print("Valores de aw promedio:", calculos_aw_promedio)

    #renderizo la plantilla pasandole los valores calculados 
    return render_template('index.html', aw_kiwi=calculos_aw_promedio["aw_kiwi"], 
                        aw_manzana=calculos_aw_promedio["aw_manzana"],
                        aw_papa=calculos_aw_promedio["aw_papa"], 
                        aw_zanahoria=calculos_aw_promedio["aw_zanahoria"], 
                        aw_fruta=calculos_aw_promedio["aw_frutas"], 
                        aw_verdura=calculos_aw_promedio["aw_verduras"], 
                        aw_total=calculos_aw_promedio["aw_total"],
                        peso_total = peso_total,
                        revisar=revisar)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)