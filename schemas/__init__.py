"""
Schemas de Pydantic
"""
from .vacante import VacanteCreate, VacanteUpdate, VacanteResponse
from .empresa import EmpresaCreate, EmpresaUpdate, EmpresaResponse
from .postulacion import PostulacionCreate, PostulacionUpdate
from .cv import CVCreate, CVResponse
from .usuario import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse,
    UsuarioLogin,
    Token,
    TokenData,
)

__all__ = [
    "VacanteCreate",
    "VacanteUpdate",
    "VacanteResponse",
    "EmpresaCreate",
    "EmpresaUpdate",
    "EmpresaResponse",
    "PostulacionCreate",
    "PostulacionUpdate",
    "CvCreate",
    "CvResponse",
    "UsuarioCreate",
    "UsuarioUpdate",
    "UsuarioResponse",
    "UsuarioLogin",
    "Token",
    "TokenData",
]
