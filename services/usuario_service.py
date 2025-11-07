"""
Service para orquestar operaciones de Usuario
"""
from sqlalchemy.orm import Session
from dao.usuario_dao import UsuarioDAO
from schemas.usuario import UsuarioCreate, UsuarioUpdate
from models.usuario import Usuario
from utils.security import get_password_hash
from typing import List, Optional
from fastapi import HTTPException, status


class UsuarioService:
    """Service para la lógica de negocio de Usuario"""

    @staticmethod
    def get_all_usuarios(db: Session, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """Obtiene todos los usuarios"""
        return UsuarioDAO.get_all(db, skip, limit)

    @staticmethod
    def get_usuario_by_id(db: Session, usuario_id: int) -> Usuario:
        """Obtiene un usuario por ID"""
        usuario = UsuarioDAO.get_by_id(db, usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {usuario_id} no encontrado"
            )
        return usuario

    @staticmethod
    def get_usuario_by_matricula(db: Session, matricula: str) -> Usuario:
        """Obtiene un usuario por matrícula"""
        usuario = UsuarioDAO.get_by_matricula(db, matricula)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con matrícula {matricula} no encontrado"
            )
        return usuario

    @staticmethod
    def create_usuario(db: Session, usuario_data: UsuarioCreate) -> Usuario:
        """Crea un nuevo usuario"""
        # Verificar que la matrícula no exista
        if UsuarioDAO.exists_matricula(db, usuario_data.matricula):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La matrícula {usuario_data.matricula} ya está registrada"
            )
        
        try:
            # Hashear la contraseña
            password_hash = get_password_hash(usuario_data.password)
            
            usuario = UsuarioDAO.create(
                db,
                nombre=usuario_data.nombre,
                apellidos=usuario_data.apellidos,
                matricula=usuario_data.matricula,
                password_hash=password_hash,
                carrera=usuario_data.carrera,
                cuatrimestre=usuario_data.cuatrimestre
            )
            return usuario
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error al crear el usuario: {str(e)}"
            )

    @staticmethod
    def update_usuario(db: Session, usuario_id: int, usuario_data: UsuarioUpdate) -> Usuario:
        """Actualiza un usuario existente"""
        # Verificar que existe
        UsuarioService.get_usuario_by_id(db, usuario_id)
        
        # Si se proporciona password, hashearlo
        password_hash = None
        if usuario_data.password:
            password_hash = get_password_hash(usuario_data.password)
        
        # Actualizar solo los campos proporcionados
        usuario = UsuarioDAO.update(
            db,
            usuario_id,
            nombre=usuario_data.nombre,
            apellidos=usuario_data.apellidos,
            carrera=usuario_data.carrera,
            cuatrimestre=usuario_data.cuatrimestre,
            password_hash=password_hash
        )
        
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al actualizar el usuario"
            )
        
        return usuario

    @staticmethod
    def delete_usuario(db: Session, usuario_id: int) -> dict:
        """Elimina un usuario"""
        # Verificar que existe
        UsuarioService.get_usuario_by_id(db, usuario_id)
        
        success = UsuarioDAO.delete(db, usuario_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al eliminar el usuario"
            )
        
        return {"message": "Usuario eliminado exitosamente"}
