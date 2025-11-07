"""
Dependencies para FastAPI (Dependency Injection)
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from dao.usuario_dao import UsuarioDAO
from utils.security import decode_access_token
from models.usuario import Usuario

# OAuth2 scheme para el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Dependency para obtener el usuario actual desde el token JWT.
    Se usa en rutas protegidas.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Decodificar token
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    matricula: str = payload.get("sub")
    if matricula is None:
        raise credentials_exception
    
    # Buscar usuario
    usuario = UsuarioDAO.get_by_matricula(db, matricula)
    if usuario is None:
        raise credentials_exception
    
    return usuario
