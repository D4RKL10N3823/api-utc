"""
Service para orquestar operaciones de Empresa
"""
from sqlalchemy.orm import Session
from dao.empresa_dao import EmpresaDAO
from schemas.empresa import EmpresaCreate, EmpresaUpdate
from models.empresa import Empresa
from typing import List
from fastapi import HTTPException, status


class EmpresaService:
    """Service para la lógica de negocio de Empresa"""

    @staticmethod
    def get_all_empresas(db: Session, skip: int = 0, limit: int = 100) -> List[Empresa]:
        """Obtiene todas las empresas"""
        return EmpresaDAO.get_all(db, skip, limit)

    @staticmethod
    def get_empresa_by_id(db: Session, empresa_id: int) -> Empresa:
        """Obtiene una empresa por ID"""
        empresa = EmpresaDAO.get_by_id(db, empresa_id)
        if not empresa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Empresa con ID {empresa_id} no encontrada"
            )
        return empresa

    @staticmethod
    def create_empresa(db: Session, empresa_data: EmpresaCreate) -> Empresa:
        """Crea una nueva empresa"""
        try:
            return EmpresaDAO.create(db, nombre=empresa_data.nombre)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error al crear la empresa: {str(e)}"
            )

    @staticmethod
    def update_empresa(db: Session, empresa_id: int, empresa_data: EmpresaUpdate) -> Empresa:
        """Actualiza los datos de una empresa"""
        EmpresaService.get_empresa_by_id(db, empresa_id)
        empresa = EmpresaDAO.update(db, empresa_id, nombre=empresa_data.nombre)
        if not empresa:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al actualizar la empresa"
            )
        return empresa

    @staticmethod
    def delete_empresa(db: Session, empresa_id: int) -> dict:
        """Elimina una empresa"""
        EmpresaService.get_empresa_by_id(db, empresa_id)
        success = EmpresaDAO.delete(db, empresa_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al eliminar la empresa"
            )
        return {"message": "Empresa eliminada exitosamente"}
