"""
DAO para operaciones de base de datos de Vacante
"""
from sqlalchemy.orm import Session
from models.vacante import Vacante
from typing import List, Optional


class VacanteDAO:
    """Data Access Object para Vacante"""

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Vacante]:
        """Obtiene todas las vacantes con paginación"""
        return db.query(Vacante).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, vacante_id: int) -> Optional[Vacante]:
        """Obtiene una vacante por ID"""
        return db.query(Vacante).filter(Vacante.id == vacante_id).first()

    @staticmethod
    def create(db: Session, nombre_empresa: str, datos_vacante: Optional[str] = None) -> Vacante:
        """Crea una nueva vacante"""
        vacante = Vacante(
            nombre_empresa=nombre_empresa,
            datos_vacante=datos_vacante
        )
        db.add(vacante)
        db.commit()
        db.refresh(vacante)
        return vacante

    @staticmethod
    def update(
        db: Session,
        vacante_id: int,
        nombre_empresa: Optional[str] = None,
        datos_vacante: Optional[str] = None
    ) -> Optional[Vacante]:
        """Actualiza una vacante existente"""
        vacante = VacanteDAO.get_by_id(db, vacante_id)
        if not vacante:
            return None

        if nombre_empresa is not None:
            vacante.nombre_empresa = nombre_empresa
        if datos_vacante is not None:
            vacante.datos_vacante = datos_vacante

        db.commit()
        db.refresh(vacante)
        return vacante

    @staticmethod
    def delete(db: Session, vacante_id: int) -> bool:
        """Elimina una vacante"""
        vacante = VacanteDAO.get_by_id(db, vacante_id)
        if not vacante:
            return False

        db.delete(vacante)
        db.commit()
        return True

    @staticmethod
    def search_by_empresa(db: Session, nombre_empresa: str) -> List[Vacante]:
        """Busca vacantes por nombre de empresa (búsqueda parcial)"""
        return db.query(Vacante).filter(
            Vacante.nombre_empresa.ilike(f"%{nombre_empresa}%")
        ).all()
