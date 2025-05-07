from modules.detector import DetectorAlimento
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria

class Cinta:
    """
    Clase que representa la cinta transportadora de la planta de alimentos.
    Toma el alimento aleatorio del detector. Luego lo coloca 
    en el cajon correspondiente.
    """
    def __init__(self, p_detector):
        """Inicializa la cinta con un detector."""
        self.__detector = p_detector

    def clasificar_alimentos(self):
        """
        Método que genera un alimento aleatorio y su peso (detectar_alimento()).
        Luego crea una instancia del alimento correspondiente(calcular_aw()).
        Return:
        - El alimento creado o None si no se detectó un alimento válido.
        """
        crear_alimento = self.__detector.detectar_alimento()
        tipo_alimento = crear_alimento['alimento']
        peso_alimento = crear_alimento['peso']

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