"""
Router para endpoints de Usuario
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from services.usuario_service import UsuarioService
from schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from dependencies import get_current_user
from models.usuario import Usuario
from typing import List

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.get("/me", response_model=UsuarioResponse)
def get_current_usuario(
    current_user: Usuario = Depends(get_current_user)
):
    """Obtiene la información del usuario actual (token)"""
    return current_user


@router.get("/", response_model=List[UsuarioResponse])
def get_all_usuarios(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de registros"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtiene todos los usuarios con paginación"""
    return UsuarioService.get_all_usuarios(db, skip, limit)


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def get_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtiene un usuario por ID"""
    return UsuarioService.get_usuario_by_id(db, usuario_id)


@router.post("/", response_model=UsuarioResponse, status_code=201)
def create_usuario(
    usuario_data: UsuarioCreate,
    db: Session = Depends(get_db)
):
    """Crea un nuevo usuario (registro público)"""
    return UsuarioService.create_usuario(db, usuario_data)


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def update_usuario(
    usuario_id: int,
    usuario_data: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Actualiza un usuario existente"""
    return UsuarioService.update_usuario(db, usuario_id, usuario_data)


@router.delete("/{usuario_id}")
def delete_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Elimina un usuario"""
    return UsuarioService.delete_usuario(db, usuario_id)
