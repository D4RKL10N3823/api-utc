"""
Schemas de Pydantic para el modelo Postulacion
"""
from pydantic import BaseModel
from datetime import date
from typing import Optional


class PostulacionBase(BaseModel):
    user_id: int
    vacante_id: int
    estado: Optional[str] = "Enviada"


class PostulacionCreate(PostulacionBase):
    pass


class PostulacionUpdate(BaseModel):
    estado: Optional[str] = None


class Postulacion(PostulacionBase):
    id: int
    fecha_postulacion: date

    class Config:
        from_attributes = True