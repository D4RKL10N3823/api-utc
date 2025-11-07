from sqlalchemy import Column, Integer, String
from database import Base  # tu clase declarativa base de SQLAlchemy

class Empresa(Base):
    __tablename__ = "empresa"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), unique=True, nullable=False)
