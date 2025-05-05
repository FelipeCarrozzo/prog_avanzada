import numpy as np
import random
import matplotlib.pyplot as plt
from modules.calculador import CalculadorBromatologico
from modules.cajon import Cajon
from modules.detector import DetectorAlimento
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria

class Cinta:
    """
    Clase que representa la cinta transportadora de la planta de alimentos.
    Toma el alimento aleatorio del detector y calcula su aw. Luego lo coloca 
    en el cajon correspondiente.
    """
    def __init__(self, detector, cajon):
        """
        Inicializa la cinta con un detector y un cajón.
        """
        self.detector = detector
        self.cajon = cajon

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
            # return None

        elif tipo_alimento == "kiwi":
            self.alimento = Kiwi(peso_alimento)

        elif tipo_alimento == "manzana":
            self.alimento = Manzana(peso_alimento)

        elif tipo_alimento == "papa":
            self.alimento = Papa(peso_alimento)

        elif tipo_alimento == "zanahoria":
            self.alimento = Zanahoria(peso_alimento)

        return self.alimento