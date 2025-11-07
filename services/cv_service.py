"""
Service para orquestar operaciones de CV
"""
from sqlalchemy.orm import Session
from dao.cv_dao import CVDAO
from schemas.cv import CVCreate
from models.cv import CV
from fastapi import HTTPException, status, UploadFile
from typing import List
from services.cv_features_service import CVFeaturesService


class CVService:
    """Service para la lógica de negocio de CV"""

    @staticmethod
    def get_all_cvs(db: Session, skip: int = 0, limit: int = 100) -> List[CV]:
        """Obtiene todos los CVs"""
        return CVDAO.get_all(db, skip, limit)

    @staticmethod
    def get_cv_by_id(db: Session, cv_id: int) -> CV:
        """Obtiene un CV por ID"""
        cv = CVDAO.get_by_id(db, cv_id)
        if not cv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"CV con ID {cv_id} no encontrado"
            )
        return cv

    @staticmethod
    def get_cvs_by_usuario(db: Session, usuario_id: int) -> List[CV]:
        """Obtiene todos los CVs de un usuario"""
        return CVDAO.get_by_usuario(db, usuario_id)

    @staticmethod
    def upload_cv(db: Session, usuario_id: int, archivo: UploadFile) -> CV:
        """Sube y guarda un nuevo CV"""
        try:
            contenido = archivo.file.read()
            cv = CVDAO.create(
                db,
                usuario_id=usuario_id,
                nombre_archivo=archivo.filename,
                tipo=archivo.content_type,
                archivo=contenido
            )
        
            CVFeaturesService.upsert_from_pdf(db, usuario_id, contenido)

            return cv
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error al subir el CV: {str(e)}"
            )

    @staticmethod
    def delete_cv(db: Session, cv_id: int) -> dict:
        """Elimina un CV"""
        CVService.get_cv_by_id(db, cv_id)
        success = CVDAO.delete(db, cv_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al eliminar el CV"
            )
        return {"message": "CV eliminado exitosamente"}
