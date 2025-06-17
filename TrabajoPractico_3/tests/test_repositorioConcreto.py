import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.repositorioConcretoBD import RepositorioUsuariosBD
from modules.usuario import Usuario
from modules.repositorioConcretoBD import RepositorioReclamosBD
from modules.reclamo import Reclamo
from modules.modelosDTO import ModeloReclamo

class TestRepositorioUsuariosBD(unittest.TestCase):
    """
    Clase de prueba para el repositorio de usuarios en la base de datos.
    Utiliza una base de datos SQLite en memoria para pruebas unitarias.
    """
    def setUp(self):
        # Crea una base de datos en memoria para pruebas
        engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=engine)
        self.__session = Session()
        self.repo = RepositorioUsuariosBD(self.__session)

    def test_guardarRegistro_y_obtenerRegistrosFiltro(self):
        usuario = Usuario(
            id=None,
            nombre="Pablo",
            apellido="Sosa",
            email="pablo@example.com",
            nombreUsuario="pablos",
            rol="UsuarioFinal",
            password="1234"
        )
        self.repo.guardarRegistro(usuario)
        resultado = self.repo.obtenerRegistrosFiltro("nombreUsuario", "pablos")
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].nombre, "Pablo")
        self.assertEqual(resultado[0].apellido, "Sosa")

    def test_actualizarAtributo(self):
        usuario = Usuario(
            id=None,
            nombre="Ana",
            apellido="García",
            email="ana@example.com",
            nombreUsuario="anag",
            rol="UsuarioFinal",
            password="abcd"
        )
        self.repo.guardarRegistro(usuario)
        # Obtener el usuario guardado
        guardado = self.repo.obtenerRegistrosFiltro("nombreUsuario", "anag")[0]
        # Actualizar el apellido
        self.repo.actualizarAtributo(guardado.id, "apellido", "Gómez")
        actualizado = self.repo.obtenerRegistrosFiltro("nombreUsuario", "anag")[0]
        self.assertEqual(actualizado.apellido, "Gómez")

class TestRepositorioReclamosBD(unittest.TestCase):
    """
    Clase de prueba para el repositorio de reclamos en la base de datos.
    Utiliza una base de datos SQLite en memoria para pruebas unitarias.
    """
    def setUp(self):
        # Crea una base de datos en memoria y una sesión nueva para cada test
        engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=engine)
        self.session = Session()
        ModeloReclamo.metadata.create_all(engine)
        self.repo = RepositorioReclamosBD(self.session)

    def test_guardar_y_obtener_registro(self):
        reclamo = Reclamo(
            id=None,
            idUsuario=1,
            fechaYHora="2025-06-17 10:00:00",
            estado="pendiente",
            tiempoResolucion=None,
            departamento="maestranza",
            numeroAdheridos=0,
            descripcion="Fuga de agua en el baño",
            imagen=None,
            usuariosAdheridos=[]
        )
        self.repo.guardarRegistro(reclamo)
        resultados = self.repo.obtenerRegistrosFiltro("departamento", "maestranza")
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0].descripcion, "Fuga de agua en el baño")

    def test_actualizar_atributo(self):
        reclamo = Reclamo(
            id=None,
            idUsuario=2,
            fechaYHora="2025-06-17 11:00:00",
            estado="pendiente",
            tiempoResolucion=None,
            departamento="soporte informático",
            numeroAdheridos=0,
            descripcion="No funciona la impresora",
            imagen=None,
            usuariosAdheridos=[]
        )
        self.repo.guardarRegistro(reclamo)
        # Obtener el id generado
        guardado = self.repo.obtenerRegistrosFiltro("descripcion", "No funciona la impresora")[0]
        self.repo.actualizarAtributo(guardado.id, "estado", "resuelto")
        actualizado = self.repo.obtenerRegistrosFiltro("id", guardado.id)[0]
        self.assertEqual(actualizado.estado, "resuelto")

    def test_obtener_registros_filtro_lista(self):
        reclamo1 = Reclamo(
            id=None,
            idUsuario=3,
            fechaYHora="2025-06-17 12:00:00",
            estado="pendiente",
            tiempoResolucion=None,
            departamento="maestranza",
            numeroAdheridos=0,
            descripcion="Luz quemada",
            imagen=None,
            usuariosAdheridos=[]
        )
        reclamo2 = Reclamo(
            id=None,
            idUsuario=4,
            fechaYHora="2025-06-17 13:00:00",
            estado="pendiente",
            tiempoResolucion=None,
            departamento="maestranza",
            numeroAdheridos=0,
            descripcion="Puerta rota",
            imagen=None,
            usuariosAdheridos=[]
        )
        self.repo.guardarRegistro(reclamo1)
        self.repo.guardarRegistro(reclamo2)
        resultados = self.repo.obtenerRegistrosFiltro("departamento", ["maestranza"])
        self.assertEqual(len(resultados), 2)
        descripciones = [r.descripcion for r in resultados]
        self.assertIn("Luz quemada", descripciones)
        self.assertIn("Puerta rota", descripciones)

if __name__ == "__main__":
    unittest.main()