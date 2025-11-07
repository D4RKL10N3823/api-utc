"""
Modelo de Vacante
"""
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from database import Base


class Vacante(Base):
    __tablename__ = "vacantes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_empresa = Column(String(255), nullable=False)
    datos_vacante = Column(Text, nullable=True)

    postulaciones = relationship("Postulacion", back_populates="vacante")

    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            "id": self.id,
            "nombre_empresa": self.nombre_empresa,
            "datos_vacante": self.datos_vacante,
        }
