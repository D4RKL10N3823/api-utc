"""
DAO para operaciones de base de datos de Empresa
"""
from sqlalchemy.orm import Session
from models.empresa import Empresa
from typing import List, Optional


class EmpresaDAO:
    """Data Access Object para Empresa"""

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Empresa]:
        """Obtiene todas las empresas con paginación"""
        return db.query(Empresa).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, empresa_id: int) -> Optional[Empresa]:
        """Obtiene una empresa por ID"""
        return db.query(Empresa).filter(Empresa.id == empresa_id).first()

    @staticmethod
    def create(db: Session, nombre: str) -> Empresa:
        """Crea una nueva empresa"""
        empresa = Empresa(nombre=nombre)
        db.add(empresa)
        db.commit()
        db.refresh(empresa)
        return empresa

    @staticmethod
    def update(db: Session, empresa_id: int, nombre: Optional[str] = None) -> Optional[Empresa]:
        """Actualiza los datos de una empresa"""
        empresa = EmpresaDAO.get_by_id(db, empresa_id)
        if not empresa:
            return None

        if nombre is not None:
            empresa.nombre = nombre

        db.commit()
        db.refresh(empresa)
        return empresa

    @staticmethod
    def delete(db: Session, empresa_id: int) -> bool:
        """Elimina una empresa"""
        empresa = EmpresaDAO.get_by_id(db, empresa_id)
        if not empresa:
            return False

        db.delete(empresa)
        db.commit()
        return True
