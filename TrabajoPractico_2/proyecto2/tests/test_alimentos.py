import unittest
from modules.alimentos import Kiwi, Manzana, Papa, Zanahoria

class TestAlimentos(unittest.TestCase):

    # Test para verificar que un Kiwi se crea correctamente con el peso y nombre adecuados
    def test_creacion_valida_kiwi(self):
        kiwi = Kiwi(0.2)
        self.assertEqual(kiwi.peso_del_alimento, 0.2)
        self.assertEqual(kiwi.nombre, "kiwi")  

    # Test para verificar que una Manzana se crea correctamente con el peso y nombre adecuados
    def test_creacion_valida_manzana(self):
        manzana = Manzana(0.4)
        self.assertEqual(manzana.peso_del_alimento, 0.4) 
        self.assertEqual(manzana.nombre, "manzana")  

    # Test para verificar que una Papa se crea correctamente con el peso y nombre adecuados
    def test_creacion_valida_papa(self):
        papa = Papa(0.3)
        self.assertEqual(papa.peso_del_alimento, 0.3)  
        self.assertEqual(papa.nombre, "papa")  

    # Test para verificar que una Zanahoria se crea correctamente con el peso y nombre adecuados
    def test_creacion_valida_zanahoria(self):
        zanahoria = Zanahoria(0.5)
        self.assertEqual(zanahoria.peso_del_alimento, 0.5)  
        self.assertEqual(zanahoria.nombre, "zanahoria")  

    # Test para verificar que se lance un ValueError si el peso está fuera del rango permitido
    def test_creacion_invalida_peso(self):
        with self.assertRaises(ValueError):  
            Kiwi(0.01) 
        with self.assertRaises(ValueError):  
            Manzana(1.0)  

    # Test para verificar que el valor de AW para un Kiwi esté en el rango [0, 1]
    def test_aw_kiwi(self):
        kiwi = Kiwi(0.2)
        aw = kiwi.calcular_aw()
        self.assertTrue(0 <= aw <= 1) 

    # Test para verificar que el valor de AW para una Manzana esté en el rango [0, 1]
    def test_aw_manzana(self):
        manzana = Manzana(0.2)
        aw = manzana.calcular_aw()
        self.assertTrue(0 <= aw <= 1)  

    # Test para verificar que el valor de AW para una Papa esté en el rango [0, 1]
    def test_aw_papa(self):
        papa = Papa(0.2)
        aw = papa.calcular_aw()
        self.assertTrue(0 <= aw <= 1)  

    # Test para verificar que el valor de AW para una Zanahoria esté en el rango [0, 1]
    def test_aw_zanahoria(self):
        zanahoria = Zanahoria(0.2)
        aw = zanahoria.calcular_aw()
        self.assertTrue(0 <= aw <= 1) 

    # Test para verificar que el valor de AW calculado para 0.2kg Kiwi sea correcto
    def test_kiwi_calcular_aw(self):
        kiwi = Kiwi(0.2)
        aw = kiwi.calcular_aw()
        self.assertAlmostEqual(aw, 0.9089, places=3)

    # Test para verificar que el valor de AW calculado para 0.4kg Manzana sea correcto
    def test_manzana_calcular_aw(self):
        manzana = Manzana(0.4)
        aw = manzana.calcular_aw()
        self.assertAlmostEqual(aw, 0.9438, places=3)  

    # Test para verificar que el valor de AW calculado para 0.3kg Papa sea correcto
    def test_papa_calcular_aw(self):
        papa = Papa(0.3)
        aw = papa.calcular_aw()
        self.assertAlmostEqual(aw, 0.9161, places=3)  

    # Test para verificar que el valor de AW calculado para 0.5kg Zanahoria sea correcto
    def test_zanahoria_calcular_aw(self):
        zanahoria = Zanahoria(0.5)
        aw = zanahoria.calcular_aw()
        self.assertAlmostEqual(aw, 0.9536, places=3)  

if __name__ == '__main__':
    unittest.main()
