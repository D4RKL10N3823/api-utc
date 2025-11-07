"""
Schemas de Pydantic para CV
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CVBase(BaseModel):
    """Schema base de CV"""
    usuario_id: int = Field(..., description="ID del usuario que sube el CV")
    nombre_archivo: str = Field(..., max_length=255, description="Nombre del archivo PDF")
    tipo: Optional[str] = Field(default="application/pdf", description="Tipo MIME del archivo")


class CVCreate(CVBase):
    """Schema para crear un nuevo CV"""
    pass


class CVResponse(CVBase):
    """Schema de respuesta de CV"""
    id: int
    fecha_subida: datetime

    class Config:
        from_attributes = True
