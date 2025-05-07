from modules.alimentos import Alimentos

class Cajon:
    """
    Clase que representa el cajón donde se depositan los alimentos.
    Contiene una lista de elementos que se reemplazan por el alimento.
    """
    def __init__(self):
        """ 
        Inicializa el cajón y una lista vacía.
        """
        self._elementos = []

    def __len__(self):
        return len(self._elementos)

    def __iter__(self):
        self._index = 0
        return self
    
    def __next__(self):
        """
        Devuelve el siguiente alimento en el cajón.
        Si no hay más alimentos, se lanza una excepción StopIteration.
        """
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
            peso_total += alimento._peso_alimento
            contador += 1
        if contador == 0:
            return 0
        return peso_total

