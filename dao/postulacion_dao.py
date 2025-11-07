"""
DAO para las operaciones de Postulacion en la base de datos
"""
from sqlalchemy.orm import Session
from models.postulacion import Postulacion
from typing import List, Optional
from datetime import date


class PostulacionDAO:
    """DAO para Postulacion"""

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Postulacion]:
        """Obtiene todas las postulaciones"""
        return db.query(Postulacion).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, postulacion_id: int) -> Optional[Postulacion]:
        """Obtiene una postulación por ID"""
        return db.query(Postulacion).filter(Postulacion.id == postulacion_id).first()

    @staticmethod
    def create(db: Session, user_id: int, vacante_id: int, estado: str) -> Postulacion:
        """Crea una nueva postulación"""
        db_postulacion = Postulacion(
            user_id=user_id,
            vacante_id=vacante_id,
            fecha_postulacion=date.today(),
            estado=estado
        )
        db.add(db_postulacion)
        db.commit()
        db.refresh(db_postulacion)
        return db_postulacion

    @staticmethod
    def update(db: Session, postulacion_id: int, estado: Optional[str] = None) -> Optional[Postulacion]:
        """Actualiza una postulación"""
        db_postulacion = PostulacionDAO.get_by_id(db, postulacion_id)
        if db_postulacion:
            if estado:
                db_postulacion.estado = estado
            db.commit()
            db.refresh(db_postulacion)
        return db_postulacion

    @staticmethod
    def delete(db: Session, postulacion_id: int) -> bool:
        """Elimina una postulación"""
        db_postulacion = PostulacionDAO.get_by_id(db, postulacion_id)
        if db_postulacion:
            db.delete(db_postulacion)
            db.commit()
            return True
        return False

    @staticmethod
    def exists(db: Session, user_id: int, vacante_id: int) -> bool:
        """Verifica si un usuario ya se postuló a una vacante"""
        return db.query(Postulacion).filter(Postulacion.user_id == user_id, Postulacion.vacante_id == vacante_id).first() is not None