from modules.alimento import Kiwi, Manzana, Papa, Zanahoria
from modules.detector import DetectorAlimento

class Cinta:
    """
    Clase que representa la cinta transportadora de la planta de alimentos.
    Toma el alimento aleatorio del detector. Luego lo coloca 
    en el cajon correspondiente.
    """
    def __init__(self, p_detector):
        """Inicializa la cinta con un detector."""
        self.__detector = p_detector #agregación

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
            alimento = None

        elif tipo_alimento == "kiwi":
            alimento = Kiwi(peso_alimento)

        elif tipo_alimento == "manzana":
            alimento = Manzana(peso_alimento)

        elif tipo_alimento == "papa":
            alimento = Papa(peso_alimento)

        elif tipo_alimento == "zanahoria":
            alimento = Zanahoria(peso_alimento)

        return alimento