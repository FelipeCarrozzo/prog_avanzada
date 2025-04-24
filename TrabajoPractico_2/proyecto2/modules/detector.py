import random
import numpy as np

class DetectorAlimento:
    """
    Clase que representa cada alimento que se puede detectar en la planta.
    Cada alimento tiene un nombre y un peso asociado.
    """
    def __init__(self):
        self.lista_alimentos = ["kiwi", "manzana", "papa", "zanahoria", "undefined"]
        self.peso_alimentos = np.round(np.linspace(0.05, 0.6, 12),2)
        self.prob_pesos = np.round(self.__softmax(self.peso_alimentos)[::-1], 2)

    def __softmax(self, x):
        """
        Función softmax para crear vector de probabilidades que sumen 1 en total
        """
        return (np.exp(x - np.max(x)) / np.exp(x - np.max(x)).sum())

    def detectar_alimento(self):
        """
        Método que simula la detección del alimento y devuelve un diccionario
        con la información del tipo y el peso del alimento.
        """
        n_alimentos = len(self.lista_alimentos)
        alimento_detectado = self.lista_alimentos[random.randint(0, n_alimentos-1)]
        peso_detectado = random.choices(self.peso_alimentos, self.prob_pesos)[0]
        # return self._crear_instancia_alimento(alimento_detectado, peso_detectado)
        return {"alimento": alimento_detectado, "peso": peso_detectado}
    

if __name__ == "__main__":
    detector = DetectorAlimento()
    for i in range(10):
        print(detector.detectar_alimento())