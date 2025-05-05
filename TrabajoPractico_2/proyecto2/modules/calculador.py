# import math
# import random
from modules.cajon import Cajon
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria
# from cajon import Cajon
# from alimentos import Kiwi, Manzana, Papa, Zanahoria, Fruta, Verdura, Alimentos


class CalculadorBromatologico:
    """
    Clase para calcular la actividad acuosa de cada alimento y
    el promedio según cada alimento, por tipo de alimento y del total
    del conjunto de alimentos.
    """
    def __init__(self, clase=None, cajon=None):
        self.clase = clase
        self.cajon = cajon
        self.promedio = None

    def calcular_aw(self, clase, cajon: Cajon):
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

        for alimento in cajon:
            if isinstance(alimento, clase):
                resultado_aw = alimento.calcular_aw()
                # resultado_aw = (resultado_aw, 2)
                resultados_aw.append(resultado_aw)
                contador += 1
    
        if contador == 0:
            return 0
        self.promedio = sum(resultados_aw) / contador
        # resultado = self.verificador_aw(promedio)
        return self.promedio
    

    def __round__(self, ndigits=None):
        resultado = self.calcular_aw()
        return round (resultado, ndigits) if ndigits is not None else round(resultado)

if __name__ == '__main__':
    alim1 = Kiwi(0.13)
    alimm1 = Kiwi(0.12)
    alimm2 = Kiwi(0.11)
    alim2 = Manzana(0.13)
    alim3 = Papa(0.13)
    alim4 = Zanahoria(0.13)
    cajon = Cajon()
    cajon.agregar_alimento(alim1)
    cajon.agregar_alimento(alimm1)
    cajon.agregar_alimento(alimm2)
    cajon.agregar_alimento(alim2)
    cajon.agregar_alimento(alim3)
    cajon.agregar_alimento(alim4)

    # calculador = CalculadorBromatologico()
    # awKiwi = calculador.calcular_aw(Kiwi, cajon)
    # awManzana = calculador.calcular_aw(Manzana, cajon)
    # awPapa = calculador.calcular_aw(Papa, cajon)
    # awZanahoria = calculador.calcular_aw(Zanahoria, cajon)
    # awFruta = calculador.calcular_aw(Fruta, cajon)
    # awVerdura = calculador.calcular_aw(Verdura, cajon)
    # awAlimentos = calculador.calcular_aw(Alimentos, cajon)
    # print(awFruta)
    # print(awVerdura)
    # print(awAlimentos)
    # print(awKiwi)
    # print(awManzana)
    # print(awPapa)
    # print(awZanahoria)