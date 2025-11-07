"""
Router para endpoints de Empresa
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from services.empresa_service import EmpresaService
from schemas.empresa import EmpresaCreate, EmpresaUpdate, EmpresaResponse
from dependencies import get_current_user
from models.usuario import Usuario
from typing import List

router = APIRouter(
    prefix="/empresas",
    tags=["Empresas"]
)


@router.get("/", response_model=List[EmpresaResponse])
def get_all_empresas(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de registros"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtiene todas las empresas con paginación"""
    return EmpresaService.get_all_empresas(db, skip, limit)


@router.get("/{empresa_id}", response_model=EmpresaResponse)
def get_empresa(
    empresa_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtiene una empresa por ID"""
    return EmpresaService.get_empresa_by_id(db, empresa_id)


@router.post("/", response_model=EmpresaResponse, status_code=201)
def create_empresa(
    empresa_data: EmpresaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Crea una nueva empresa"""
    return EmpresaService.create_empresa(db, empresa_data)


@router.put("/{empresa_id}", response_model=EmpresaResponse)
def update_empresa(
    empresa_id: int,
    empresa_data: EmpresaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Actualiza una empresa existente"""
    return EmpresaService.update_empresa(db, empresa_id, empresa_data)


@router.delete("/{empresa_id}")
def delete_empresa(
    empresa_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Elimina una empresa"""
    return EmpresaService.delete_empresa(db, empresa_id)
