"""
Router para endpoints de Vacante
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from services.vacante_service import VacanteService
from schemas.vacante import VacanteCreate, VacanteUpdate, VacanteResponse
from dependencies import get_current_user
from models.usuario import Usuario
from typing import List

router = APIRouter(
    prefix="/vacantes",
    tags=["Vacantes"]
)


@router.get("/", response_model=List[VacanteResponse])
def get_all_vacantes(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de registros"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtiene todas las vacantes con paginación"""
    return VacanteService.get_all_vacantes(db, skip, limit)


@router.get("/search", response_model=List[VacanteResponse])
def search_vacantes(
    empresa: str = Query(..., description="Nombre de la empresa a buscar"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Busca vacantes por nombre de empresa"""
    return VacanteService.search_vacantes_by_empresa(db, empresa)


@router.get("/{vacante_id}", response_model=VacanteResponse)
def get_vacante(
    vacante_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtiene una vacante por ID"""
    return VacanteService.get_vacante_by_id(db, vacante_id)


@router.post("/", response_model=VacanteResponse, status_code=201)
def create_vacante(
    vacante_data: VacanteCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Crea una nueva vacante"""
    return VacanteService.create_vacante(db, vacante_data)


@router.put("/{vacante_id}", response_model=VacanteResponse)
def update_vacante(
    vacante_id: int,
    vacante_data: VacanteUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Actualiza una vacante existente"""
    return VacanteService.update_vacante(db, vacante_id, vacante_data)


@router.delete("/{vacante_id}")
def delete_vacante(
    vacante_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Elimina una vacante"""
    return VacanteService.delete_vacante(db, vacante_id)
