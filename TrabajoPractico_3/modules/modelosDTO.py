"""MODELOS DATA TRANSFER OBJECT"""
#dependencias

from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text
from sqlalchemy.orm import relationship,  declarative_base

Base = declarative_base()

class ModeloUsuario(Base):
    """Modelo de usuario para la base de datos.
    Representa un usuario en el sistema con atributos como nombre, apellido,
    email, nombre de usuario, rol y contraseña.
    """
    __tablename__ = 'Usuarios'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    nombreUsuario = Column(String(20), nullable=False, unique=True)
    # claustro = Column(String(20), nullable=False)
    rol = Column(String(20), nullable=True, default=None)
    password = Column(String(20))
    # departamento = Column(String(20), nullable=True, default=None)

class ModeloReclamo(Base):
    """Modelo de reclamo para la base de datos.
    Representa un reclamo en el sistema con atributos como fecha y hora,
    estado, tiempo de resolución, departamento, usuario creador, número de adheridos,
    descripción, imagen y número de adheridos.
    """
    __tablename__ = 'Reclamos'
    id = Column(Integer(), primary_key=True)
    fechaYHora = Column(String(50), nullable=False)  # Formato de fecha y hora
    estado = Column(String(20), nullable=False, default='pendiente')
    tiempoResolucion = Column(Integer, nullable=True, default=None)
    departamento = Column(String(20), nullable=False)
    usuarioCreador = Column(Integer, ForeignKey('Usuarios.id'), nullable=False)
    numeroAdheridos = Column(Integer, nullable=False, default=0)
    # usuariosAdheridos = relationship('ModeloUsuario', secondary='reclamos_usuarios')
    descripcion = Column(Text, nullable=False)
    imagen = Column(String(255), nullable=True)
    numeroAdheridos = Column(Integer, nullable=False, default=0)