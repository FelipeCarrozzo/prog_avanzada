import math
import random

class CalculadorBromatologico:
    def __init__(self, alimento):
        self.alimento = alimento
        self.resultados = {}
        # self.calcular_composicion()
        self.rangos_m = {
            "manzana": (4.0, 6.0),
            "kiwi": (3.0, 5.0),
            "papa": (2.0, 3.5),
            "zanahoria": (5.0, 7.0)
        }

    def verificador_aw(self):
        if self.aw < 0.2 or self.aw > 1:
            return "aw fuera de rango válido (0.2 - 1.0)"

        if self.aw >= 0.90:
            return "El alimento no es apto para el consumo"
        else:
            return "Alimento apto para el consumo"

    def calcular_aw(self):
        if self.alimento not in self.rangos_m:
            raise ValueError("No se reconoce como alimento")
        
        self.m = random.uniform(*self.rangos_m[self.alimento])

        if self.alimento == "manzana":
            self.manzana = 0.97 * ((15 * self.m)**2) / (1 + (15 * self.m)**2)
            self.aw = self.manzana
        elif self.alimento == "kiwi":
            exp_term = math.exp(-18 * self.m)
            self.kiwi = 0.96 * (1 - exp_term) / (1 + exp_term)
            self.aw = self.kiwi
        elif self.alimento == "papa":
            self.papa = 0.66 * math.atan(18 * self.m)
            self.aw = self.papa
            return self.aw
        elif self.alimento == "zanahoria":
            self.zanahoria = 0.96 * (1 - math.exp(-10 * self.m))
            self.aw = self.zanahoria
            # return self.aw

        resultado = self.verificador_aw()
        return f"{resultado} | m = {round(self.m, 3)} kg/kg | aw = {round(self.aw, 3)}"
if __name__ == '__main__':
    for alimento in ["papa"]:
        calculador = CalculadorBromatologico(alimento)
        aw = calculador.calcular_aw()
        print(f"Alimento: {alimento.capitalize()} | {aw}")


        # m = round(random.uniform(*calculador.rangos_m[alimento]), 3)
        # print(f"{alimento.capitalize():<10} | m = {m} kg/kg | aw = {aw}")