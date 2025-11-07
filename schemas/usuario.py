"""
Schemas de Pydantic para Usuario
"""
from pydantic import BaseModel, Field
from typing import Optional


class UsuarioBase(BaseModel):
    """Schema base de Usuario"""
    nombre: str = Field(..., max_length=100, description="Nombre del usuario")
    apellidos: str = Field(..., max_length=100, description="Apellidos del usuario")
    matricula: str = Field(..., max_length=20, description="Matrícula única del usuario")
    carrera: Optional[str] = Field(None, max_length=150, description="Carrera del usuario")
    cuatrimestre: Optional[int] = Field(None, ge=1, le=12, description="Cuatrimestre actual")


class UsuarioCreate(UsuarioBase):
    """Schema para crear un usuario"""
    password: str = Field(..., min_length=6, description="Contraseña del usuario")


class UsuarioUpdate(BaseModel):
    """Schema para actualizar un usuario"""
    nombre: Optional[str] = Field(None, max_length=100)
    apellidos: Optional[str] = Field(None, max_length=100)
    carrera: Optional[str] = Field(None, max_length=150)
    cuatrimestre: Optional[int] = Field(None, ge=1, le=12)
    password: Optional[str] = Field(None, min_length=6)


class UsuarioResponse(UsuarioBase):
    """Schema de respuesta de Usuario"""
    id: int

    class Config:
        from_attributes = True


class UsuarioLogin(BaseModel):
    """Schema para login"""
    matricula: str = Field(..., description="Matrícula del usuario")
    password: str = Field(..., description="Contraseña del usuario")


class Token(BaseModel):
    """Schema de respuesta de token"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema de datos del token"""
    matricula: Optional[str] = None
