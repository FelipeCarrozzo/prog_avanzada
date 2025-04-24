import numpy as np
import random
import matplotlib.pyplot as plt
from calculador import CalculadorBromatologico
from cajon import Cajon
from alimentos import Kiwi, Manzana, Papa, Zanahoria, AlimentoInvalido
from detector import DetectorAlimento

class Cinta:
    """
    Clase que representa la cinta transportadora de la planta de alimentos.
    Toma el alimento aleatorio del detector y calcula su aw. Luego lo coloca 
    en el cajon correspondiente.
    """
    def __init__(self, n_elementos:int, detector, cajon):
        self.elementos = n_elementos #variable para hacer la cantidad exacta de alimentos ingresados
        self.detector = detector
        self.cajon = cajon
        # self.calculador = calculador

    def clasificar_alimentos(self):
        """
        Método que genera un alimento aleatorio y su peso (detectar_alimento()).
        Luego crea una instancia del alimento correspondiente(calcular_aw()).
        Return:
        - El alimento creado o None si no se detectó un alimento válido.
        """
        crear_alimento = self.detector.detectar_alimento()
        tipo_alimento = crear_alimento['alimento']
        peso_alimento = crear_alimento['peso']
        print("Salida: ", crear_alimento)

        if tipo_alimento == "undefined":
            self.alimento = None

        elif tipo_alimento == "kiwi":
            self.alimento = Kiwi(peso_alimento)

        elif tipo_alimento == "manzana":
            self.alimento = Manzana(peso_alimento)

        elif tipo_alimento == "papa":
            self.alimento = Papa(peso_alimento)

        elif tipo_alimento == "zanahoria":
            self.alimento = Zanahoria(peso_alimento)

        return self.alimento


if __name__ == "__main__":
    detector = DetectorAlimento()
    cajon  = Cajon(1)
    cinta = Cinta(5, detector, cajon)
    print(cinta.clasificar_alimentos())