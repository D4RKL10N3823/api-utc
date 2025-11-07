"""
DAO para operaciones de base de datos de CV
"""
from sqlalchemy.orm import Session
from models.cv import CV
from typing import List, Optional


class CVDAO:
    """Data Access Object para CV"""

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[CV]:
        """Obtiene todos los CVs"""
        return db.query(CV).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, cv_id: int) -> Optional[CV]:
        """Obtiene un CV por su ID"""
        return db.query(CV).filter(CV.id == cv_id).first()

    @staticmethod
    def get_by_usuario(db: Session, usuario_id: int) -> List[CV]:
        """Obtiene todos los CVs de un usuario específico"""
        return db.query(CV).filter(CV.usuario_id == usuario_id).all()

    @staticmethod
    def create(db: Session, usuario_id: int, nombre_archivo: str, tipo: str, archivo: bytes) -> CV:
        """Crea un nuevo CV"""
        cv = CV(
            usuario_id=usuario_id,
            nombre_archivo=nombre_archivo,
            tipo=tipo,
            archivo=archivo
        )
        db.add(cv)
        db.commit()
        db.refresh(cv)
        return cv

    @staticmethod
    def delete(db: Session, cv_id: int) -> bool:
        """Elimina un CV por ID"""
        cv = CVDAO.get_by_id(db, cv_id)
        if not cv:
            return False

        db.delete(cv)
        db.commit()
        return True
