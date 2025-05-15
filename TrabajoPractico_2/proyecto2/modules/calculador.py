from modules.cajon import Cajon
from modules.alimento import Alimento

class CalculadorBromatologico:
    """
    Clase para calcular la actividad acuosa de cada alimento y
    el promedio según cada alimento, por tipo de alimento y del total
    del conjunto de alimentos.
    """
    def __init__(self):
        """
        Inicializa la clase CalculadorBromatologico.
        Se le puede pasar un tipo de alimento y un cajón.
        """
        self.__promedio = None

    def calcular_aw(self, p_clase: Alimento, p_cajon: Cajon):
        """
        Método que calcula el promedio de la actividad acuosa de los alimentos.
        Se verifica que no sea mayor a 1 o menor a 0. 
        Args:
        - Para el promedio de cada alimento: clase = (Manzana|Kiwi|Papa|Zanahoria)
        - Para el promedio del tipo de alimento: clase = (Fruta|Verdura)
        - Para el promedio de todos los alimentos: clase = Alimentos
        Returns:
        - El promedio de la actividad acuosa de los alimentos

        """
        resultados_aw = []
        contador = 0

        for alimento in p_cajon:
            if isinstance(alimento, p_clase):
                resultado_aw = alimento.calcular_aw()
                resultados_aw.append(resultado_aw)
                contador += 1
    
        if contador == 0:
            return 0
        self.__promedio = sum(resultados_aw) / contador
        return self.__promedio
    
    def calcular_peso(self, p_cajon: Cajon):
        """
        Método que calcula el peso total de los alimentos existentes en un cajón.
        Args:
        - p_cajon: El cajón que contiene los alimentos.
        Returns:
        - El peso total de los alimentos en el cajón.
        """
        peso_total = 0
        contador = 0
        for alimento in p_cajon:
            peso_total += alimento.peso
            contador += 1
        if contador == 0:
            return 0
        return peso_total

    def __round__(self, ndigits=None):
        """
        Método que redondea el resultado de la actividad acuosa.
        Args:
        - ndigits: Número de decimales a los que se desea redondear.
        Returns:
        - El resultado redondeado a la cantidad de decimales especificada.
        """
        resultado = self.calcular_aw()
        return round (resultado, ndigits) if ndigits is not None else round(resultado)