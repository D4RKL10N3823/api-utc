"""
Schemas de Pydantic para Vacante
"""
from pydantic import BaseModel, Field
from typing import Optional, Any, List


class VacanteBase(BaseModel):
    """Schema base de Vacante"""
    nombre_empresa: str = Field(..., max_length=255, description="Nombre de la empresa")
    datos_vacante: Optional[Any] = Field(None, description="Datos de la vacante")


class VacanteCreate(VacanteBase):
    """Schema para crear una vacante"""
    pass


class VacanteUpdate(BaseModel):
    """Schema para actualizar una vacante"""
    nombre_empresa: Optional[str] = Field(None, max_length=255)
    datos_vacante: Optional[Any] = Field(None, description="Datos de la vacante (JSON)")


class VacanteResponse(VacanteBase):
    """Schema de respuesta de Vacante"""
    id: int

    match_score: Optional[float] = None
    match_cos: Optional[float] = None
    match_bm25: Optional[float] = None
    match_overlap: float | None = None
    match_terms: Optional[List[str]] = None

    class Config:
        from_attributes = True
