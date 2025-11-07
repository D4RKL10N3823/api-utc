"""
Service para orquestar operaciones de Postulacion
"""
from sqlalchemy.orm import Session
from dao.postulacion_dao import PostulacionDAO
from schemas.postulacion import PostulacionCreate, PostulacionUpdate
from models.postulacion import Postulacion
from services.usuario_service import UsuarioService
from services.vacante_service import VacanteService
from typing import List
from fastapi import HTTPException, status


class PostulacionService:
    """Service para la lógica de negocio de Postulacion"""

    @staticmethod
    def get_all_postulaciones(db: Session, skip: int = 0, limit: int = 100) -> List[Postulacion]:
        """Obtiene todas las postulaciones"""
        return PostulacionDAO.get_all(db, skip, limit)

    @staticmethod
    def get_postulacion_by_id(db: Session, postulacion_id: int) -> Postulacion:
        """Obtiene una postulación por ID"""
        postulacion = PostulacionDAO.get_by_id(db, postulacion_id)
        if not postulacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Postulación con ID {postulacion_id} no encontrada"
            )
        return postulacion

    @staticmethod
    def create_postulacion(db: Session, postulacion_data: PostulacionCreate) -> Postulacion:
        """Crea una nueva postulación"""
        # Verificar que el usuario y la vacante existan
        UsuarioService.get_usuario_by_id(db, postulacion_data.user_id)
        VacanteService.get_vacante_by_id(db, postulacion_data.vacante_id)

        # Verificar que el usuario no se haya postulado ya a esta vacante
        if PostulacionDAO.exists(db, postulacion_data.user_id, postulacion_data.vacante_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya se ha postulado a esta vacante"
            )

        try:
            postulacion = PostulacionDAO.create(
                db,
                user_id=postulacion_data.user_id,
                vacante_id=postulacion_data.vacante_id,
                estado=postulacion_data.estado
            )
            return postulacion
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error al crear la postulación: {str(e)}"
            )

    @staticmethod
    def update_postulacion(db: Session, postulacion_id: int, postulacion_data: PostulacionUpdate) -> Postulacion:
        """Actualiza el estado de una postulación"""
        PostulacionService.get_postulacion_by_id(db, postulacion_id)
        
        postulacion = PostulacionDAO.update(db, postulacion_id, estado=postulacion_data.estado)
        if not postulacion:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al actualizar la postulación")
        return postulacion

    @staticmethod
    def delete_postulacion(db: Session, postulacion_id: int) -> dict:
        """Elimina una postulación"""
        PostulacionService.get_postulacion_by_id(db, postulacion_id)
        
        if not PostulacionDAO.delete(db, postulacion_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al eliminar la postulación")
        
        return {"message": "Postulación eliminada exitosamente"}