from modules.repositorioConcretoBD import RepositorioUsuariosBD
from modules.config import crear_engine

def crear_repositorio():
    session = crear_engine()
    repoUsuarios =  RepositorioUsuariosBD(session())
    # repoReclamos = RepositorioReclamos(session())
    return repoUsuarios