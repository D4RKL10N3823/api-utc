from sqlalchemy import Column, BigInteger, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from database import Base
from pgvector.sqlalchemy import Vector 

class CVFeatures(Base):
    __tablename__ = "cv_features"
    usuario_id = Column(BigInteger, ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True)
    texto = Column(Text, nullable=False)
    skills = Column(JSONB, nullable=False, default=list)
    embedding = Column(Vector(1024), nullable=False) 
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class VacanteFeatures(Base):
    __tablename__ = "vacante_features"
    vacante_id = Column(BigInteger, ForeignKey("vacantes.id", ondelete="CASCADE"), primary_key=True)
    jd_text = Column(Text, nullable=False)
    jd_terms = Column(JSONB, nullable=False, default=list)
    embedding = Column(Vector(1024), nullable=False) 
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
