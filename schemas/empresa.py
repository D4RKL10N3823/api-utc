"""
Schemas de Pydantic para Empresa
"""
from pydantic import BaseModel, Field
from typing import Optional


class EmpresaBase(BaseModel):
    """Schema base de Empresa"""
    nombre: str = Field(..., max_length=255, description="Nombre de la empresa")


class EmpresaCreate(EmpresaBase):
    """Schema para crear una empresa"""
    pass


class EmpresaUpdate(BaseModel):
    """Schema para actualizar una empresa"""
    nombre: Optional[str] = Field(None, max_length=255)


class EmpresaResponse(EmpresaBase):
    """Schema de respuesta de Empresa"""
    id: int

    class Config:
        from_attributes = True
