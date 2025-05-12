import unittest
from modules.alimento import Kiwi, Manzana, Papa, Zanahoria
from modules.cajon import Cajon
from modules.cinta import Cinta
from modules.detector import DetectorAlimento

class TestCinta(unittest.TestCase):

    def test_clasificar_alimento(self):
        n_alimentos = 10
        detector = DetectorAlimento()  
        cinta = Cinta(detector)
        cajon = Cajon()
        
        while len(cajon) < n_alimentos:
            alimento = cinta.clasificar_alimentos()
            if alimento is not None:
                cajon.agregar_alimento(alimento)
        
        self.assertEqual(len(cajon), n_alimentos)

        for alimento in cajon:
            self.assertIsNotNone(alimento, "El alimento es None")
            self.assertTrue(
                isinstance(alimento, (Kiwi, Manzana, Papa, Zanahoria)),
                f"Tipo de alimento inesperado: {type(alimento)}"
            )
            self.assertGreater(alimento.peso, 0, "El peso del alimento debe ser mayor que 0")
            self.assertLessEqual(alimento.peso, 1000, "El peso del alimento debe ser menor o igual a 1000")

if __name__ == '__main__':
    unittest.main()