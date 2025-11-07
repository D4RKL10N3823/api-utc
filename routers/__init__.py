"""
Routers de FastAPI
"""
from .vacante_router import router as vacante_router
from .usuario_router import router as usuario_router
from .auth_router import router as auth_router

__all__ = ["vacante_router", "usuario_router", "auth_router"]
