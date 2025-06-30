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
        """Crea una base de datos SQLite en memoria antes de cada test."""
        engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=engine)
        self.__session = Session()
        self.repo = RepositorioUsuariosBD(self.__session)

    def test_guardarRegistro_y_obtenerRegistrosFiltro(self):
        """
        Verifica que un usuario guardado pueda recuperarse correctamente
        usando un filtro por nombre de usuario.
        """
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
        """
        Verifica que se pueda actualizar un atributo específico de un usuario
        (por ejemplo, cambiar el apellido).
        """
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

    def test_obtenerRegistroFiltro_no_encontrado(self):
        """
        Verifica que al buscar un usuario con un nombre de usuario que no existe,
        el resultado sea None.
        """
        resultado = self.repo.obtenerRegistroFiltro("nombreUsuario", "noexiste")
        self.assertIsNone(resultado)

    def test_eliminarRegistro_existente(self):
        """
        Verifica que se pueda eliminar un usuario existente de la base de datos.
        """
        usuario = Usuario(None, "Juan", "Perez", "jp@example.com", "juanp", "UsuarioFinal", "pass")
        self.repo.guardarRegistro(usuario)
        guardado = self.repo.obtenerRegistrosFiltro("nombreUsuario", "juanp")[0]
        self.assertTrue(self.repo.eliminarRegistro(guardado.id))
        self.assertEqual(self.repo.obtenerRegistrosFiltro("nombreUsuario", "juanp"), [])

    def test_eliminarRegistro_inexistente(self):
        """
        Verifica que al intentar eliminar un usuario con un ID inexistente,
        el método retorne False.
        """
        self.assertFalse(self.repo.eliminarRegistro(9999))

class TestRepositorioReclamosBD(unittest.TestCase):
    """
    Clase de prueba para el repositorio de reclamos en la base de datos.
    Utiliza una base de datos SQLite en memoria para pruebas unitarias.
    """
    def setUp(self):
        """Crea la base en memoria y genera la tabla de reclamos antes de cada test."""
        engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=engine)
        self.session = Session()
        ModeloReclamo.metadata.create_all(engine)
        self.repo = RepositorioReclamosBD(self.session)

    def test_guardar_y_obtener_registro(self):
        """
        Verifica que un reclamo guardado se pueda recuperar correctamente
        filtrando por el campo 'departamento'.
        """
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
        """
        Verifica que se pueda actualizar el estado de un reclamo ya guardado.
        """
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
        guardado = self.repo.obtenerRegistrosFiltro("descripcion", "No funciona la impresora")[0]
        self.repo.actualizarAtributo(guardado.id, "estado", "resuelto")
        actualizado = self.repo.obtenerRegistrosFiltro("id", guardado.id)[0]
        self.assertEqual(actualizado.estado, "resuelto")

    def test_obtener_registros_filtro_lista(self):
        """
        Verifica que se puedan recuperar múltiples reclamos cuando se filtra
        por una lista de valores (por ejemplo, varios departamentos).
        """
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

    def test_eliminarRegistro_existente(self):
        """
        Verifica que se pueda eliminar un reclamo existente de la base de datos.
        """
        reclamo = Reclamo(None, 1, "2025-06-17 10:00:00", "pendiente", None, "maestranza", 0, "Test reclamo", None, [])
        self.repo.guardarRegistro(reclamo)
        guardado = self.repo.obtenerRegistrosFiltro("descripcion", "Test reclamo")[0]
        self.assertTrue(self.repo.eliminarRegistro(guardado.id))
        self.assertEqual(self.repo.obtenerRegistrosFiltro("descripcion", "Test reclamo"), [])

    def test_eliminarRegistro_inexistente(self):
        """
        Verifica que al intentar eliminar un reclamo con un ID inexistente,
        el método retorne False.
        """
        self.assertFalse(self.repo.eliminarRegistro(9999))

    def test_obtenerRegistroFiltro_no_encontrado(self):
        """
        Verifica que al buscar un reclamo con una descripción inexistente,
        se retorne None.
        """
        resultado = self.repo.obtenerRegistroFiltro("descripcion", "noexiste")
        self.assertIsNone(resultado)

    def test_agregarUsuarioAReclamo(self):
        """
        Verifica que se pueda adherir un usuario a un reclamo y que no se pueda
        adherir el mismo usuario más de una vez al mismo reclamo.
        """
        usuario = Usuario(None, "Mario", "Lopez", "mario@example.com", "mariol", "UsuarioFinal", "pass")
        from modules.repositorioConcretoBD import RepositorioUsuariosBD
        repoUsuarios = RepositorioUsuariosBD(self.session)
        repoUsuarios.guardarRegistro(usuario)
        usuario_db = repoUsuarios.obtenerRegistrosFiltro("nombreUsuario", "mariol")[0]

        reclamo = Reclamo(None, usuario_db.id, "2025-06-17 10:00:00", "pendiente", None, "maestranza", 0, "Reclamo test", None, [])
        self.repo.guardarRegistro(reclamo)
        reclamo_db = self.repo.obtenerRegistrosFiltro("descripcion", "Reclamo test")[0]

        self.assertTrue(self.repo.agregarUsuarioAReclamo(reclamo_db.id, usuario_db))
        #Se intenta adherir de nuevo (debe devolver False)
        self.assertFalse(self.repo.agregarUsuarioAReclamo(reclamo_db.id, usuario_db))

if __name__ == "__main__":
    unittest.main()