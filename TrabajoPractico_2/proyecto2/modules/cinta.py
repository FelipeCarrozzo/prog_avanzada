import numpy as np
import random
import matplotlib.pyplot as plt
from calculador import CalculadorBromatologico
from alimentos import Kiwi, Manzana, Papa, Zanahoria, AlimentoInvalido

class Cinta:
    """Clase que representa la cinta transportadora de la planta de alimentos.
    Toma el alimento aleatorio del detector y calcula su aw. Luego lo coloca 
    en el cajon correspondiente."""
    def __init__(self, n_elementos, detector, cajon, calculador=None):
        self.elementos = n_elementos #variable para hacer la cantidad exacta de alimentos ingresados
        self.detector = detector
        self.cajon = cajon
        self.calculador = calculador

    def agregar_alimento(self):
        """Método que genera un alimento aleatorio y su peso (detectar_alimento()).
        Luego crea una instancia del alimento correspondiente y calcula su aw (calcular_aw()).
        """
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
            
            #aca se deberia agregar al cajón. El resultado del prom aw es eliminatorio?

            print(f"se detectó {instancia_alimento.nombre} con -> {resultado_aw} de aw")

class DetectorAlimento:
    """Clase que representa cada alimento que se puede detectar en la planta.
    Cada alimento tiene un nombre y un peso asociado.
    """
    def __init__(self):
        self.alimentos = ["kiwi", "manzana", "papa", "zanahoria", "undefined"]
        self.peso_alimentos = np.round(np.linspace(0.05, 0.6, 12),2)
        self.prob_pesos = np.round(self.__softmax(self.peso_alimentos)[::-1], 2)

    def __softmax(self, x):
        """Función softmax para crear vector de probabilidades que sumen 1 en total
        """
        return (np.exp(x - np.max(x)) / np.exp(x - np.max(x)).sum())

    def detectar_alimento(self):
        """Método que simula la detección del alimento y devuelve un diccionario
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
    """Clase que representa el cajón donde se depositan los alimentos.
    Contiene una lista de elementos que se reemplazan por el alimento.
    """
    def __init__(self, n_elementos):
        self.elementos = [None] * n_elementos #lista con n_elementos que se reemplazan por el alimento


if __name__ == "__main__":
    detector = DetectorAlimento()
    cajon = Cajon(n_elementos=10)
    cinta = Cinta(n_elementos=10, detector=detector, cajon=cajon)
    cinta.agregar_alimento()