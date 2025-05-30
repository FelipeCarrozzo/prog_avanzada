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