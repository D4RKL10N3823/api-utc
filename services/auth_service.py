"""
Service para autenticación y autorización
"""
from datetime import timedelta
from sqlalchemy.orm import Session
from dao.usuario_dao import UsuarioDAO
from schemas.usuario import UsuarioLogin, Token
from utils.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import HTTPException, status


class AuthService:
    """Service para la lógica de autenticación"""

    @staticmethod
    def authenticate_user(db: Session, login_data: UsuarioLogin) -> Token:
        """Autentica un usuario y retorna un token JWT"""
        # Buscar usuario por matrícula
        usuario = UsuarioDAO.get_by_matricula(db, login_data.matricula)
        
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Matrícula o contraseña incorrecta",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verificar contraseña
        if not verify_password(login_data.password, usuario.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Matrícula o contraseña incorrecta",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Crear token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": usuario.matricula, "id": usuario.id},
            expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token, token_type="bearer")
