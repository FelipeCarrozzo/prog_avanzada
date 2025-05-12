import unittest
from modules.cajon import Cajon
from modules.alimento import Kiwi, Manzana, Papa, Zanahoria, Fruta, Verdura, Alimento
from modules.calculador import CalculadorBromatologico

class TestCalculadorBromatologico(unittest.TestCase):
    """
    Esta clase contiene los test unitarios para verificar el comportamiento
    del calculador bromatológico en base a los alimentos presentes en un cajón.
    Cada test verifica el cálculo del promedio de agua (aw) para diferentes
    categorías de alimentos en el cajón.
    """

    def setUp(self):
        """
        Configura el entorno inicial para los tests.
        Se crean instancias de alimentos (Kiwi, Manzana, Papa, Zanahoria) y
        se agregan al cajón. También se instancia el calculador bromatológico.
        """
        self.kiwi1 = Kiwi(0.13)
        self.kiwi2 = Kiwi(0.12)
        self.kiwi3 = Kiwi(0.11)
        self.manzana = Manzana(0.13)
        self.papa1 = Papa(0.14)
        self.papa2 = Papa(0.12)
        self.papa3 = Papa(0.10)
        self.zanahoria = Zanahoria(0.11)

        self.cajon = Cajon()
        self.cajon.agregar_alimento(self.kiwi1)
        self.cajon.agregar_alimento(self.kiwi2)
        self.cajon.agregar_alimento(self.kiwi3)
        self.cajon.agregar_alimento(self.manzana)
        self.cajon.agregar_alimento(self.papa1)
        self.cajon.agregar_alimento(self.papa2)
        self.cajon.agregar_alimento(self.papa3)
        self.cajon.agregar_alimento(self.zanahoria)

        self.calculador = CalculadorBromatologico()

    def test_promedio_kiwis(self):
        """
        Verifica que el promedio del agua (aw) de los kiwis en el cajón
        sea el esperado, calculado como el promedio de los aw individuales
        de los tres kiwis.
        """
        aw = self.calculador.calcular_aw(Kiwi, self.cajon)
        expected = (self.kiwi1.calcular_aw() + self.kiwi2.calcular_aw() + self.kiwi3.calcular_aw()) / 3
        self.assertAlmostEqual(aw, expected, places=4)

    def test_promedio_manzana(self):
        """
        Verifica que el promedio del agua (aw) de las manzanas en el cajón
        coincida con el valor del aw individual de la manzana.
        """
        aw = self.calculador.calcular_aw(Manzana, self.cajon)
        expected = self.manzana.calcular_aw()
        self.assertAlmostEqual(aw, expected, places=4)

    def test_promedio_papa(self):
        """
        Verifica que el promedio del agua (aw) de las papas en el cajón
        coincida con el valor del aw individual de la papa.
        """
        aw = self.calculador.calcular_aw(Papa, self.cajon)
        expected = (self.papa1.calcular_aw() + self.papa2.calcular_aw() + self.papa3.calcular_aw()) / 3
        self.assertAlmostEqual(aw, expected, places=4)

    def test_promedio_zanahoria(self):
        """
        Verifica que el promedio del agua (aw) de las zanahorias en el cajón
        coincida con el valor del aw individual de la zanahoria.
        """
        aw = self.calculador.calcular_aw(Zanahoria, self.cajon)
        expected = self.zanahoria.calcular_aw()
        self.assertAlmostEqual(aw, expected, places=4)

    def test_promedio_frutas(self):
        """
        Verifica que el promedio del agua (aw) de las frutas en el cajón
        sea el esperado, calculado como el promedio de los aw de los kiwis
        y las manzanas.
        """
        aw = self.calculador.calcular_aw(Fruta, self.cajon)
        expected = (
            self.kiwi1.calcular_aw() +
            self.kiwi2.calcular_aw() +
            self.kiwi3.calcular_aw() +
            self.manzana.calcular_aw()
        ) / 4
        self.assertAlmostEqual(aw, expected, places=4)

    def test_promedio_verduras(self):
        """
        Verifica que el promedio del agua (aw) de las verduras en el cajón
        sea el esperado, calculado como el promedio de los aw de las papas
        y las zanahorias.
        """
        aw = self.calculador.calcular_aw(Verdura, self.cajon)
        expected = (self.papa1.calcular_aw() + self.papa2.calcular_aw() + self.papa3.calcular_aw() + self.zanahoria.calcular_aw()) / 4
        self.assertAlmostEqual(aw, expected, places=4)

    def test_promedio_total_alimentos(self):
        """
        Verifica que el promedio del agua (aw) de todos los alimentos en el
        cajón coincida con el valor esperado, calculado como el promedio
        de los aw individuales de todos los alimentos en el cajón.
        """
        aw = self.calculador.calcular_aw(Alimento, self.cajon)
        total_aw = sum([a.calcular_aw() for a in self.cajon])
        expected = total_aw / len(self.cajon)
        self.assertAlmostEqual(aw, expected, places=4)

    def test_clase_sin_alimentos(self):
        """
        Verifica que si se solicita calcular el promedio del agua (aw) para
        una clase de alimento que no está presente en el cajón (en este caso,
        una clase ficticia), el valor devuelto sea 0.
        """
        class Ficticio(Alimento): pass
        aw = self.calculador.calcular_aw(Ficticio, self.cajon)
        self.assertEqual(aw, 0)
    
    def test_calcular_peso_total(self):
        """
        Verifica que el cálculo del peso total de los alimentos en el cajón
        sea correcto, sumando los pesos individuales.
        """
        peso = self.calculador.calcular_peso(self.cajon)
        expected = sum([a.peso for a in self.cajon])
        self.assertAlmostEqual(peso, expected, places=4)


if __name__ == "__main__":
    unittest.main()
