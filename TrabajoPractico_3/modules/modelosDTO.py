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
    claustro = Column(String(20), nullable=False)
    rol = Column(String(20), nullable=False)
    nombreUsuario = Column(String(20), nullable=False, unique = True)
    email = Column(String(100), nullable=False, unique = True)
    password = Column (String (20))
    departamento = Column(String(20))


