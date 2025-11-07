"""
DAO para operaciones de base de datos de Usuario
"""
from sqlalchemy.orm import Session
from models.usuario import Usuario
from typing import List, Optional


class UsuarioDAO:
    """Data Access Object para Usuario"""

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """Obtiene todos los usuarios con paginación"""
        return db.query(Usuario).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, usuario_id: int) -> Optional[Usuario]:
        """Obtiene un usuario por ID"""
        return db.query(Usuario).filter(Usuario.id == usuario_id).first()

    @staticmethod
    def get_by_matricula(db: Session, matricula: str) -> Optional[Usuario]:
        """Obtiene un usuario por matrícula"""
        return db.query(Usuario).filter(Usuario.matricula == matricula).first()

    @staticmethod
    def create(
        db: Session,
        nombre: str,
        apellidos: str,
        matricula: str,
        password_hash: str,
        carrera: Optional[str] = None,
        cuatrimestre: Optional[int] = None
    ) -> Usuario:
        """Crea un nuevo usuario"""
        usuario = Usuario(
            nombre=nombre,
            apellidos=apellidos,
            matricula=matricula,
            password_hash=password_hash,
            carrera=carrera,
            cuatrimestre=cuatrimestre
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario

    @staticmethod
    def update(
        db: Session,
        usuario_id: int,
        nombre: Optional[str] = None,
        apellidos: Optional[str] = None,
        carrera: Optional[str] = None,
        cuatrimestre: Optional[int] = None,
        password_hash: Optional[str] = None
    ) -> Optional[Usuario]:
        """Actualiza un usuario existente"""
        usuario = UsuarioDAO.get_by_id(db, usuario_id)
        if not usuario:
            return None

        if nombre is not None:
            usuario.nombre = nombre
        if apellidos is not None:
            usuario.apellidos = apellidos
        if carrera is not None:
            usuario.carrera = carrera
        if cuatrimestre is not None:
            usuario.cuatrimestre = cuatrimestre
        if password_hash is not None:
            usuario.password_hash = password_hash

        db.commit()
        db.refresh(usuario)
        return usuario

    @staticmethod
    def delete(db: Session, usuario_id: int) -> bool:
        """Elimina un usuario"""
        usuario = UsuarioDAO.get_by_id(db, usuario_id)
        if not usuario:
            return False

        db.delete(usuario)
        db.commit()
        return True

    @staticmethod
    def exists_matricula(db: Session, matricula: str) -> bool:
        """Verifica si existe una matrícula"""
        return db.query(Usuario).filter(Usuario.matricula == matricula).first() is not None
