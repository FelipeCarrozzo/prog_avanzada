from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria, Alimentos
# from alimentos import Kiwi, Manzana, Papa, Zanahoria, Alimentos
class Cajon: #podria reemplazarse por bolson
    """
    Clase que representa el cajón donde se depositan los alimentos.
    Contiene una lista de elementos que se reemplazan por el alimento.
    """
    def __init__(self):
        self.valor = 0
        self._elementos = [] 

    def __len__(self):
        return len(self._elementos)

    def __iter__(self):
        self._index = 0
        return self
    
    def __next__(self):
        if self._index < len(self._elementos):
                    result = self._elementos[self._index]
                    self._index += 1
                    return result
        else:
            raise StopIteration
    
    def agregar_alimento(self, alimento: Alimentos):
        """
        Método que agrega un alimento al cajón reemplazando los valores None.
        Verifica que el alimento sea del tipo correcto y que el cajón no esté lleno.
        """
        if not isinstance(alimento, Alimentos):
            raise TypeError("Solo se pueden agregar objetos de tipo Alimento")
        self._elementos.append(alimento)

    def mostrar_contenido_cajon(self):
        return self._elementos
    
    def calcular_peso(self):
        """
        Método que calcula el peso total de los alimentos existentes en un cajón.
        """
        peso_total = 0
        contador = 0
        for alimento in self._elementos:
            peso_total += alimento.peso
            contador += 1
        if contador == 0:
            return 0
        return peso_total

if __name__ == "__main__":
    kiwi = Kiwi(0.20)
    manzana = Manzana(0.20)
    papa = Papa(0.20)
    zanahoria = Zanahoria(0.20)
    cajon = Cajon(5)
    cajon.agregar_alimento(papa) #agrega un alimento al cajon
    cajon.agregar_alimento(kiwi) #agrega un alimento al cajon
    cajon.agregar_alimento(manzana) #agrega un alimento al cajon
    cajon.agregar_alimento(zanahoria) #agrega un alimento al cajon
    print(cajon.mostrar_contenido_cajon()) #imprime la lista de elementos del cajon