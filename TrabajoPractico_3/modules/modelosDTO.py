"""MODELOS DATA TRANSFER OBJECT"""
#dependencias

from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text
from sqlalchemy.orm import relationship,  declarative_base

Base = declarative_base()

class ModeloUsuario(Base):
    __tablename__ = 'Usuarios'
    id = Column(Integer(), primary_key=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    nombreUsuario = Column(String(20), nullable=False, unique=True)
    claustro = Column(String(20), nullable=False)
    password = Column(String(20))
    rol = Column(String(20), nullable=True, default=None)
    departamento = Column(String(20), nullable=True, default=None)

class ModeloReclamo(Base):
    __tablename__ = 'Reclamos'
    id = Column(Integer(), primary_key=True)
    fechaYHora = Column(String(50), nullable=False)  # Formato de fecha y hora
    estado = Column(String(20), nullable=False, default='pendiente')
    tiempoResolucion = Column(Integer, nullable=True, default=None)
    departamento = Column(String(20), nullable=False)
    usuarioCreador = Column(Integer, ForeignKey('Usuarios.id'), nullable=False)
    numeroAdheridos = Column(Integer, nullable=False, default=0)
    usuariosAdheridos = relationship('ModeloUsuario', secondary='reclamos_usuarios')
    descripcion = Column(Text, nullable=False)
    imagen = Column(String(255), nullable=True)
    numeroAdheridos = Column(Integer, nullable=False, default=0)