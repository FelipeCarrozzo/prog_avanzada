# import math
# import random
from modules.cajon import Cajon
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria, AlimentoInvalido

class CalculadorBromatologico:
    """
    Clase para calcular la actividad acuosa de cada alimento y
    el promedio según cada alimento, por tipo de alimento y del total
    del conjunto de alimentos.
    """
    def __init__(self):
        pass

    def verificador_aw(self, resultado):
        """
        Método que verifica si la actividad acuosa está dentro del rango válido (0 - 1.0).
        Si no lo está, devuelve un mensaje indicando que el alimento no es apto para el consumo.
        """
        if resultado < 0 or resultado > 1:
            return "aw fuera de rango válido (0 - 1.0)"

        if resultado >= 0.90:
            return "El alimento no es apto para el consumo"
        else:
            return resultado
    
    def aw_prom(self, clase, cajon: Cajon):
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
        resultado_aw = 0
        contador = 0

        for alimento in cajon:
            if isinstance(alimento, clase):
                resultado_aw += alimento.calcular_aw()
                resultado_aw = round(resultado_aw, 2)
                contador += 1
            if contador == 0:
                return 0
        promedio = resultado_aw / contador
        resultado = self.verificador_aw(promedio)
        return resultado

if __name__ == '__main__':
    alim = Kiwi(0.13)
    cajon = Cajon(5)
    cajon.agregar_alimento(alim)
    calculador = CalculadorBromatologico()
    aw = calculador.aw_prom(Kiwi, cajon)
    print(f"Alimento: {type(alim).__name__} | {aw}")
