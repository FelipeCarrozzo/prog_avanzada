import numpy as np
import random
import matplotlib.pyplot as plt

class Cinta:
    """ clase que representa la cinta transportadora de la planta de alimentos.
    toma el alimento aleatorio del detector y lo coloca en el cajon correspondiente."""
    def __init__(self, n_elementos):
        self.iteraciones = n_elementos #variable para hacer la cantidad exacta de alimentos ingresados
        self.detector = DetectorAlimento()
        self.cajon = Cajon(n_elementos)


    def agregar_alimento(self):
        """método que agrega un alimento al cajon correspondiente."""
        for i in range(self.iteraciones):
            alimento = self.detector.detectar_alimento()
            if self.cajon.elementos[i] is None:
                self.cajon.elementos[i] = alimento
            else:
                break


    def mostrar_cajon(self):
        """método que muestra el estado actual del cajón."""
        print(f'Estado del cajón: {self.cajon.elementos}')


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
        return {"alimento": alimento_detectado, "peso": peso_detectado}
    
class Cajon: #podria reemplazarse por bolson
    def __init__(self, n_elementos):
        self.elementos = [None] * n_elementos #lista con n_elementos que se reemplazan por el alimento


if __name__ == "__main__":
    # random.seed(1)
    # sensor = DetectorAlimento()
    # lista_pesos = []
    
    # for _ in range(10):
    #     lista_pesos.append(sensor.detectar_alimento()["peso"])

    # plt.hist(lista_pesos, bins=12)
    # plt.xlabel('Peso (kg)')
    # plt.ylabel('Frecuencia')
    # plt.title('Histograma de Pesos de Alimentos')
    # plt.show()
    cinta = Cinta(2)
    cinta.agregar_alimento()
    cinta.mostrar_cajon()