import numpy as np
import random
import matplotlib.pyplot as plt
from calculador import CalculadorBromatologico
from alimentos import Kiwi, Manzana, Papa, Zanahoria, AlimentoInvalido

class Cinta:
    """ clase que representa la cinta transportadora de la planta de alimentos.
    toma el alimento aleatorio del detector y lo coloca en el cajon correspondiente."""
    def __init__(self, n_elementos, detector, cajon, calculador=None):
        self.elementos = n_elementos #variable para hacer la cantidad exacta de alimentos ingresados
        self.detector = detector
        self.cajon = cajon
        self.calculador = calculador

    def agregar_alimento(self):
        """método que agrega un alimento al cajon correspondiente."""
        for i in range(self.elementos):
            crear_alimento = self.detector.detectar_alimento()
            print("Salida: ", crear_alimento)
            instancia_alimento = self.detector.crear_instancia_alimento(crear_alimento["alimento"], crear_alimento["peso"])

            if isinstance(instancia_alimento, AlimentoInvalido):
                print("Alimento inválido detectado, se omite el cálculo.")
                continue  # o lo que quieras hacer

            #calulador
            calculador = CalculadorBromatologico(instancia_alimento.nombre)
            resultado_aw = calculador.calcular_aw()
            
            print(f"se detectó {instancia_alimento.nombre} con -> {resultado_aw} de aw")

class DetectorAlimento:
    """clase que representa un conjunto de sensores de la cinta transportadora
    para detectar el tipo de alimento y su peso.
    """
    def __init__(self):
        self.alimentos = ["kiwi", "manzana", "papa", "zanahoria", "undefined"]
        self.peso_alimentos = np.round(np.linspace(0.05, 0.6, 12),2)
        self.prob_pesos = np.round(self.__softmax(self.peso_alimentos)[::-1], 2)

    def __softmax(self, x):
        """función softmax para crear vector de probabilidades 
        que sumen 1 en total
        """
        return (np.exp(x - np.max(x)) / np.exp(x - np.max(x)).sum())

    def detectar_alimento(self):
        """método que simula la detección del alimento y devuelve un diccionario
        con la información del tipo y el peso del alimento.
        """
        n_alimentos = len(self.alimentos)
        alimento_detectado = self.alimentos[random.randint(0, n_alimentos-1)]
        peso_detectado = random.choices(self.peso_alimentos, self.prob_pesos)[0]
        # return self._crear_instancia_alimento(alimento_detectado, peso_detectado)
        return {"alimento": alimento_detectado, "peso": peso_detectado}
    
    def crear_instancia_alimento(self, nombre, peso):
        clases = {
            "kiwi": Kiwi,
            "manzana": Manzana,
            "papa": Papa,
            "zanahoria": Zanahoria,
        }
        clase = clases.get(nombre, AlimentoInvalido)

        return clase(peso)
    
class Cajon: #podria reemplazarse por bolson
    def __init__(self, n_elementos):
        self.elementos = [None] * n_elementos #lista con n_elementos que se reemplazan por el alimento


if __name__ == "__main__":
    detector = DetectorAlimento()
    cajon = Cajon(n_elementos=10)
    cinta = Cinta(n_elementos=10, detector=detector, cajon=cajon)
    cinta.agregar_alimento()