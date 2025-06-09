from modules.modelosDTO import Base
from modules.repositorioConcretoBD import RepositorioReclamosBD
from modules.config import crear_engine

# Crear la base de datos y las tablas
engine = crear_engine()
Base.metadata.create_all(engine)
