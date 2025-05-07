from abc import ABC, abstractmethod
import math 
import numpy as np 


class Alimentos(ABC):
    """
    Clase abstracta que representa un alimento.
    Contiene un atributo de peso y un método abstracto para calcular la actividad acuosa
    (aw) en cada tipo de alimento.
    """
    def __init__(self, p_peso_alimento):
        if 0.05<=p_peso_alimento <= 0.6:
            self.__peso_alimento = p_peso_alimento
        else:
            raise ValueError ("El peso no se encuentra dentro de los límites establecidos (0.05kg - 0.6kg)")

    @property
    def peso_alimento(self):
        return self.__peso_alimento
    
    @abstractmethod 
    def calcular_aw(self):
        pass 

class Fruta(Alimentos, ABC):
    """
    Clase abstracta que representa una fruta.
    Hereda de la clase Alimentos y contiene un método abstracto para calcular la actividad acuosa (aw).
    """
    def __init__(self, p_peso_alimento):
        super().__init__(p_peso_alimento)
        
    @abstractmethod
    def calcular_aw(self):
        pass

class Verdura(Alimentos, ABC):
    """
    Clase abstracta que representa una verdura.
    Hereda de la clase Alimentos y contiene un método abstracto para calcular la actividad acuosa (aw).
    """
    def __init__(self, p_peso_alimento):
        super().__init__(p_peso_alimento)

    @abstractmethod
    def calcular_aw(self):
        pass

class Kiwi(Fruta):
    def __init__(self, p_peso_alimento):
        """
        Clase que hereda sus atributos de Fruta que a la vez hereda sus atributos de Alimentos 
        """
        super().__init__(p_peso_alimento)


    def calcular_aw(self):
        """
        Método que calcula la actividad acuosa del Kiwi
        """
        awk = 0.96 * ((1 - math.exp(-18 * self.peso_alimento)) / (1 + math.exp(-18 * self.peso_alimento)))
        return(awk)
    
    def __str__(self):
        """
        Método que devuelve una cadena de texto que incluye el nombre y el peso del alimento
        """
        return(f"Kiwi ({self.__peso_alimento}kg)")
    
    @property
    def nombre(self):
        return "kiwi"

class Manzana(Fruta):
    def __init__(self, p_peso_alimento):
        """
        Clase que hereda sus atributos de Fruta que a la vez hereda sus atributos de Alimentos 
        """
        super().__init__(p_peso_alimento)
        
    def calcular_aw(self):
        """
        Método que calcula la actividad acuosa de la Manzana
        """
        awm = 0.97 * ((15 * self.peso_alimento) ** 2) / (1 + (15 * self.peso_alimento) ** 2)
        return(awm)

    def __str__(self):
        """
        Método que devuelve una cadena de texto que incluye el nombre y el peso del alimento
        """
        return(f"Manzana ({self.__peso_alimento}kg)")
    
    @property
    def nombre(self):
        return "manzana"

class Papa(Verdura):
    def __init__(self, p_peso_alimento):
        """
        Clase que hereda sus atributos de Verdura que a la vez hereda sus atributos de Alimentos 
        """
        super().__init__(p_peso_alimento)
    
    def calcular_aw(self):
        """
        Método que calcula la actividad acuosa de la Papa
        """
        awp = 0.66 * (np.arctan(18 * self.peso_alimento))
        return(awp)

    def __str__(self):
        """
        Método que devuelve una cadena de texto que incluye el nombre y el peso del alimento
        """
        return(f"Papa ({self.__peso_alimento}kg)")
    
    @property
    def nombre(self):
        return "papa"

class Zanahoria(Verdura):
    def __init__(self, p_peso_alimento):
        """-
        Clase que hereda sus atributos de Verdura que a la vez hereda sus atributos de Alimentos 
        """
        super().__init__(p_peso_alimento)
 
    def calcular_aw(self):
        """
        Método que calcula la actividad acuosa de la Zanahoria
        """
        awz = 0.96 * ((1 - math.exp(-10 * self.peso_alimento)))
        return(awz)

    def __str__(self):
        """
        Método que devuelve una cadena de texto que incluye el nombre y el peso del alimento
        """
        return f"Zanahoria ({self.__peso_alimento}kg)"
    
    @property
    def nombre(self):
        return "zanahoria"