"""
Modelo de Usuario
"""
from sqlalchemy import Column, Integer, String, SmallInteger
from database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    matricula = Column(String(20), unique=True, nullable=False, index=True)
    carrera = Column(String(150), nullable=True)
    cuatrimestre = Column(SmallInteger, nullable=True)
    password_hash = Column(String(255), nullable=False)  # Para el auth

    def to_dict(self):
        """Convierte el modelo a diccionario (sin password)"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellidos": self.apellidos,
            "matricula": self.matricula,
            "carrera": self.carrera,
            "cuatrimestre": self.cuatrimestre,
        }
