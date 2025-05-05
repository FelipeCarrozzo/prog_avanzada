from abc import ABC, abstractmethod
import math 
import numpy as np 

"""clases abstractas"""

class Alimentos(ABC):
    def __init__(self, peso_alimento):
        if 0.05<=peso_alimento <= 0.6:
            self._peso_alimento = peso_alimento
        else:
            raise ValueError ("el peso no se encuentra dentro de los parámetros.")

    @property
    def peso_del_alimento(self):
        return self._peso_alimento
    
    @abstractmethod 
    def calcular_aw(self):
        pass 

class Fruta(Alimentos, ABC):
    def __init__(self, peso_alimento):
        super().__init__(peso_alimento)
        
    @abstractmethod
    def calcular_aw(self):
        pass

class Verdura(Alimentos, ABC):
    def __init__(self, peso_alimento):
        super().__init__(peso_alimento)

    @abstractmethod
    def calcular_aw(self):
        pass

class Kiwi(Fruta):
    def __init__(self, peso_alimento):
        """clase que hereda sus atributos de Fruta que a la vez hereda sus atributos de Alimentos 
        """
        super().__init__(peso_alimento)


    def calcular_aw(self):
        """método que calcula la actividad acuosa del Kiwi
        """
        awk = 0.96 * ((1 - math.exp(-18 * self.peso_del_alimento)) / (1 + math.exp(-18 * self.peso_del_alimento)))
        return(awk)
    
    def __str__(self):
        """método que devuelve una cadena de texto que incluye el nombre y el peso del alimento
        """
        return(f"Kiwi ({self._peso_alimento}kg)")
    
    @property
    def nombre(self):
        return "kiwi"

class Manzana(Fruta):
    def __init__(self, peso_alimento):
        """Clase que hereda sus atributos de Fruta que a la vez hereda sus atributos de Alimentos 
        """
        super().__init__(peso_alimento)
        
    def calcular_aw(self):
        """método que calcula la actividad acuosa de la Manzana
        """
        awm = 0.97 * ((15 * self.peso_del_alimento) ** 2) / (1 + (15 * self.peso_del_alimento) ** 2)
        return(awm)

    def __str__(self):
        """método que devuelve una cadena de texto que incluye el nombre y el peso del alimento
        """
        return(f"Manzana ({self._peso_alimento}kg)")
    
    @property
    def nombre(self):
        return "manzana"

class Papa(Verdura):
    def __init__(self, peso_alimento):
        """clase que hereda sus atributos de Verdura que a la vez hereda sus atributos de Alimentos 
        """
        super().__init__(peso_alimento)
    
    def calcular_aw(self):
        """método que calcula la actividad acuosa de la Papa
        """
        awp = 0.66 * (np.arctan(18 * self.peso_del_alimento))
        return(awp)

    def __str__(self):
        """método que devuelve una cadena de texto que incluye el nombre y el peso del alimento
        """
        return(f"Papa ({self._peso_alimento}kg)")
    
    @property
    def nombre(self):
        return "papa"

class Zanahoria(Verdura):
    def __init__(self, peso_alimento):
        """clase que hereda sus atributos de Verdura que a la vez hereda sus atributos de Alimentos 
        """
        super().__init__(peso_alimento)
 
    def calcular_aw(self):
        """método que calcula la actividad acuosa de la Zanahoria
        """
        awz = 0.96 * ((1 - math.exp(-10 * self.peso_del_alimento)))
        return(awz)

    def __str__(self):
        """método que devuelve una cadena de texto que incluye el nombre y el peso del alimento
        """
        return f"Zanahoria ({self._peso_alimento}kg)"
    
    @property
    def nombre(self):
        return "zanahoria"