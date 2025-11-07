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
    db: Session = Depends(get_db),
    usuario_id: int | None = Query(None, description="ID"),
    topk: int = 100,
    orden: str = "probabilidad",
    metrics: bool = False
):
    """
    Obtiene todas las vacantes.
    Si se pasa un usuario_id válido y orden='probabilidad', las ordena de mayor a menor match.
    """
    if usuario_id and orden == "probabilidad":
        return VacanteService.list_for_user_ranked(db, usuario_id, topk=topk, with_metrics=metrics)
    return VacanteService.get_all_vacantes(db, limit=topk)


@router.get("/general", response_model=List[VacanteResponse])
def get_all_vacantes_general(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de registros"),
    db: Session = Depends(get_db)
):
    """
    Obtiene todas las vacantes directamente de la base de datos.
    Sin filtros ni ordenamiento por probabilidad, solo paginación básica.
    """
    return VacanteService.get_all_vacantes(db, skip=skip, limit=limit)


@router.get("/search", response_model=List[VacanteResponse])
def search_vacantes(
    empresa: str = Query(..., description="Nombre de la empresa a buscar"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user) # Este get_current_user viene de auth_service
):
    """Busca vacantes por nombre de empresa"""
    return VacanteService.search_vacantes_by_empresa(db, empresa)


@router.get("/{vacante_id}", response_model=VacanteResponse)
def get_vacante(
    vacante_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user) # Este get_current_user viene de auth_service
):
    """Obtiene una vacante por ID"""
    return VacanteService.get_vacante_by_id(db, vacante_id)


@router.post("/", response_model=VacanteResponse, status_code=201)
def create_vacante(
    vacante_data: VacanteCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user) # Este get_current_user viene de auth_service
):
    """Crea una nueva vacante"""
    return VacanteService.create_vacante(db, vacante_data)


@router.put("/{vacante_id}", response_model=VacanteResponse)
def update_vacante(
    vacante_id: int,
    vacante_data: VacanteUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user) # Este get_current_user viene de auth_service
):
    """Actualiza una vacante existente"""
    return VacanteService.update_vacante(db, vacante_id, vacante_data)


@router.delete("/{vacante_id}")
def delete_vacante(
    vacante_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user) # Este get_current_user viene de auth_service
):
    """Elimina una vacante"""
    return VacanteService.delete_vacante(db, vacante_id)
