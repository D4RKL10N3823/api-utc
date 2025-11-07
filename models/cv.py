"""
Modelo SQLAlchemy para CV
"""
from sqlalchemy import Column, Integer, String, LargeBinary, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from database import Base


class CV(Base):
    __tablename__ = "cv"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    nombre_archivo = Column(String(255), nullable=False)
    tipo = Column(String(100), default="application/pdf")
    archivo = Column(LargeBinary, nullable=False)
    fecha_subida = Column(TIMESTAMP(timezone=False), server_default=func.now())
