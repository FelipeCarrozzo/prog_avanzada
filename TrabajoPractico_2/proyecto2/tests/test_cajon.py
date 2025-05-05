import unittest
from modules.alimentos import Kiwi, Papa
from modules.cajon import Cajon

class TestCajon(unittest.TestCase):
    def setUp(self):
        # Crea una instancia vacía de Cajon y dos alimentos válidos (Kiwi y Papa)
        self.cajon = Cajon()
        self.kiwi = Kiwi(0.2)
        self.papa = Papa(0.3)

    def test_agregar_alimento(self):
        """
        Verifica que se puede agregar un alimento válido (instancia de clase alimento) al cajón.
        Luego se comprueba que el alimento efectivamente está dentro del contenido del cajón.
        """
        self.cajon.agregar_alimento(self.kiwi)
        self.assertIn(self.kiwi, self.cajon.mostrar_contenido_cajon())

    def test_tipo_incorrecto(self):
        """
        Verifica que al intentar agregar un objeto que no es del tipo 'Alimento' (por ejemplo, un string),
        el método 'agregar_alimento' lanza un TypeError.
        """
        with self.assertRaises(TypeError):
            self.cajon.agregar_alimento("no es un alimento")

    def test_calcular_peso(self):
        """
        Agrega dos alimentos al cajón y verifica que el método 'calcular_peso'
        devuelve la suma correcta del peso de ambos alimentos.
        """
        self.cajon.agregar_alimento(self.kiwi)
        self.cajon.agregar_alimento(self.papa)
        peso = self.cajon.calcular_peso()
        self.assertAlmostEqual(peso, 0.5)

    def test_iterador(self):
        """
        Verifica que el cajón es iterable y que al recorrerlo se obtienen los objetos
        agregados en el orden esperado.
        """
        self.cajon.agregar_alimento(self.kiwi)
        items = [al for al in self.cajon]
        self.assertEqual(items, [self.kiwi])
