#dependencias
from modules.repositorioConcretoBD import RepositorioUsuariosBD
from modules.config import crear_engine

def crearRepositorio():
    """Crea una instancia de repositorios"""
    session = crear_engine() # Crear una clase Session de SQLAlchemy
    repoUsuarios =  RepositorioUsuariosBD(session()) # crear una instancia de sesión de base de datos
    # repoReclamos = RepositorioReclamos(session())
    return repoUsuarios