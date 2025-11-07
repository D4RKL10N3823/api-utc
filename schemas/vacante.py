"""
Schemas de Pydantic para Vacante
"""
from pydantic import BaseModel, Field
from typing import Optional


class VacanteBase(BaseModel):
    """Schema base de Vacante"""
    nombre_empresa: str = Field(..., max_length=255, description="Nombre de la empresa")
    datos_vacante: Optional[str] = Field(None, description="Datos de la vacante")


class VacanteCreate(VacanteBase):
    """Schema para crear una vacante"""
    pass


class VacanteUpdate(BaseModel):
    """Schema para actualizar una vacante"""
    nombre_empresa: Optional[str] = Field(None, max_length=255)
    datos_vacante: Optional[str] = None


class VacanteResponse(VacanteBase):
    """Schema de respuesta de Vacante"""
    id: int

    class Config:
        from_attributes = True
