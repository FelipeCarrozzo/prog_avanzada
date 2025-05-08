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
        self.__elementos = []

    def __len__(self):
        return len(self.__elementos)

    def __iter__(self):
        self._index = 0
        return self
    
    def __next__(self):
        """
        Devuelve el siguiente alimento en el cajón.
        Si no hay más alimentos, se lanza una excepción StopIteration.
        """
        if self._index < len(self.__elementos):
                    result = self.__elementos[self._index]
                    self._index += 1
                    return result
        else:
            raise StopIteration
    
    def agregar_alimento(self, p_alimento: Alimentos):
        """
        Método que agrega un alimento al cajón reemplazando los valores None.
        Verifica que el alimento sea del tipo correcto y que el cajón no esté lleno.
        """
        if not isinstance(p_alimento, Alimentos):
            raise TypeError("Solo se pueden agregar objetos de tipo Alimento")
        self.__elementos.append(p_alimento)