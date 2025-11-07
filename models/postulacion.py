"""
Modelo de Postulacion
"""
from sqlalchemy import Column, Integer, Date, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import date


class Postulacion(Base):
    __tablename__ = "postulaciones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    vacante_id = Column(Integer, ForeignKey("vacantes.id"), nullable=False)
    fecha_postulacion = Column(Date, nullable=False, default=date.today)
    estado = Column(String(50), nullable=False, default="Enviada")

    usuario = relationship("Usuario", back_populates="postulaciones")
    vacante = relationship("Vacante", back_populates="postulaciones")