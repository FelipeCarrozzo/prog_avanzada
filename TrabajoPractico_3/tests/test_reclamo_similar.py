import unittest
from modules.gestorReclamos import GestorReclamos
from modules.reclamo import Reclamo

#arrange
class FakeRepo:
    def __init__(self, reclamos):
        self._reclamos = reclamos
    def obtenerRegistrosFiltro(self, campo, valor):
        # Solo filtra por departamento en este caso
        if campo == "departamento":
            return [r for r in self._reclamos if r.departamento == (valor[0] if isinstance(valor, list) else valor)]
        return []

class FakeClasificador:
    def clasificar(self, descripciones):
        # Devuelve un departamento fijo para test
        return ["Mantenimiento"]

class ReclamoTest(Reclamo):
    def __init__(self, id, descripcion, estado="pendiente"):
        super().__init__(id=id, idUsuario=1, fechaYHora="2024-06-11 10:00:00", estado=estado, tiempoResolucion=None,
                         departamento="Mantenimiento", numeroAdheridos=0, descripcion=descripcion, imagen=None, usuariosAdheridos=[])

class TestObtenerReclamosSimilares(unittest.TestCase):
    def setUp(self):
        #act
        reclamos = [
            ReclamoTest(1, "El proyector del aula 2 no funciona"),
            ReclamoTest(2, "No anda la luz en el aula 2"),
            ReclamoTest(3, "El proyector del aula 2 funciona bien", estado="resuelto"),
            ReclamoTest(4, "Problema con el aire acondicionado"),
            ReclamoTest(5, "Problema con la impresora"),
        ]
        self.repo = FakeRepo(reclamos)
        self.gestor = GestorReclamos(self.repo)
        self.gestor._GestorReclamos__clasificador = FakeClasificador()  # inyecta clasificador fake

    def test_similares(self):
        #arrange
        datos = {"descripcion": "El proyector del aula 2 no funciona"}
        #act
        resultado = self.gestor.obtenerReclamosSimilares(datos)
        descripciones = [r["descripcion"] for r in resultado]
        #assert
        self.assertEqual(len(resultado), 1)
        self.assertIn("El proyector del aula 2 no funciona", descripciones)
        self.assertNotIn("El proyector del aula 2 funciona bien", descripciones)  # está resuelto
        self.assertNotIn("No anda la luz en el aula 2", descripciones)  # poco similar

if __name__ == "__main__":
    unittest.main()
