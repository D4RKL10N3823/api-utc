"""
Service para orquestar operaciones de Vacante
"""
from sqlalchemy.orm import Session
from dao.vacante_dao import VacanteDAO
from schemas.vacante import VacanteCreate, VacanteUpdate
from models.vacante import Vacante
from typing import List, Optional
from fastapi import HTTPException, status


class VacanteService:
    """Service para la lógica de negocio de Vacante"""

    @staticmethod
    def get_all_vacantes(db: Session, skip: int = 0, limit: int = 100) -> List[Vacante]:
        """Obtiene todas las vacantes"""
        return VacanteDAO.get_all(db, skip, limit)

    @staticmethod
    def get_vacante_by_id(db: Session, vacante_id: int) -> Vacante:
        """Obtiene una vacante por ID"""
        vacante = VacanteDAO.get_by_id(db, vacante_id)
        if not vacante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vacante con ID {vacante_id} no encontrada"
            )
        return vacante

    @staticmethod
    def create_vacante(db: Session, vacante_data: VacanteCreate) -> Vacante:
        """Crea una nueva vacante"""
        try:
            vacante = VacanteDAO.create(
                db,
                nombre_empresa=vacante_data.nombre_empresa,
                datos_vacante=vacante_data.datos_vacante
            )
            return vacante
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error al crear la vacante: {str(e)}"
            )

    @staticmethod
    def update_vacante(db: Session, vacante_id: int, vacante_data: VacanteUpdate) -> Vacante:
        """Actualiza una vacante existente"""
        # Verificar que existe
        VacanteService.get_vacante_by_id(db, vacante_id)
        
        # Actualizar solo los campos proporcionados
        vacante = VacanteDAO.update(
            db,
            vacante_id,
            nombre_empresa=vacante_data.nombre_empresa,
            datos_vacante=vacante_data.datos_vacante
        )
        
        if not vacante:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al actualizar la vacante"
            )
        
        return vacante

    @staticmethod
    def delete_vacante(db: Session, vacante_id: int) -> dict:
        """Elimina una vacante"""
        # Verificar que existe
        VacanteService.get_vacante_by_id(db, vacante_id)
        
        success = VacanteDAO.delete(db, vacante_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al eliminar la vacante"
            )
        
        return {"message": "Vacante eliminada exitosamente"}

    @staticmethod
    def search_vacantes_by_empresa(db: Session, nombre_empresa: str) -> List[Vacante]:
        """Busca vacantes por nombre de empresa"""
        return VacanteDAO.search_by_empresa(db, nombre_empresa)
