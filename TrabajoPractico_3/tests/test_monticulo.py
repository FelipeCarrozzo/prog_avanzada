import unittest
from modules.monticulos import MonticuloMediana, MonticuloBinario

class TestMonticuloBinario(unittest.TestCase):
    
    def test_insertar_min(self):
        """Test para insertar valores en un montículo mínimo."""
        monticulo = MonticuloBinario("min")
        for valor in [5, 3, 8, 1]:
            monticulo.insertar(valor)
        self.assertEqual(monticulo.devolverListaValores()[1], 1)

    def test_insertar_max(self):
        """Test para insertar valores en un montículo máximo."""
        #arrange
        monticulo = MonticuloBinario("max")
        for valor in [5, 3, 8, 1]:
            #act
            monticulo.insertar(valor)
        #assert
        self.assertEqual(monticulo.devolverListaValores()[1], 8)

    def test_eliminar_min(self):
        """Test para eliminar el valor mínimo de un montículo mínimo."""
        monticulo = MonticuloBinario("min")
        for valor in [4, 2, 7, 1]:
            monticulo.insertar(valor)
        minimo = monticulo.eliminarMinOMax()
        self.assertEqual(minimo, 1)
        self.assertEqual(monticulo.devolverListaValores()[1], 2)

    def test_eliminar_max(self):
        """Test para eliminar el valor máximo de un montículo máximo."""
        monticulo = MonticuloBinario("max")
        for valor in [4, 2, 7, 1]:
            monticulo.insertar(valor)
        maximo = monticulo.eliminarMinOMax()
        self.assertEqual(maximo, 7)
        self.assertEqual(monticulo.devolverListaValores()[1], 4)

    def test_vacio(self):
        """Test para intentar eliminar de un montículo vacío."""
        monticulo = MonticuloBinario("min")
        with self.assertRaises(ValueError):
            monticulo.eliminarMinOMax()


class TestMonticuloMediana(unittest.TestCase):

    def setUp(self):
        self.m = MonticuloMediana()

    def test_mediana_incremental(self):
        """Test para verificar la mediana al agregar valores de forma incremental."""
        #arrange
        secuencia = [5, 15, 1, 3, 8, 12, 7, 9, 4]
        esperado = [5, 10.0, 5, 4.0, 5, 6.5, 7, 7.5, 7]
        for i, valor in enumerate(secuencia):
            #act
            self.m.agregarValor(valor)
            #assert
            self.assertAlmostEqual(self.m.obtenerMediana(), esperado[i])

    def test_insertar_y_obtener_mediana(self):
        """Test para insertar valores y verificar la mediana en diferentes etapas."""
        #act
        self.m.agregarValor(5)
        #assert
        self.assertEqual(self.m.obtenerMediana(), 5)

        self.m.agregarValor(10)
        self.assertEqual(self.m.obtenerMediana(), 7.5)

        self.m.agregarValor(2)
        self.assertEqual(self.m.obtenerMediana(), 5)

        self.m.agregarValor(15)
        self.assertEqual(self.m.obtenerMediana(), 7.5)

        self.m.agregarValor(20)
        self.assertEqual(self.m.obtenerMediana(), 10)

    def test_vacio(self):
        """Test para intentar obtener la mediana de un montículo vacío."""

        with self.assertRaises(ValueError):
            self.m.obtenerMediana()

if __name__ == "__main__":
    unittest.main()