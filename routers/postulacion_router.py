"""
Router para los endpoints de Postulacion
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas.postulacion import Postulacion, PostulacionCreate, PostulacionUpdate
from services.postulacion_service import PostulacionService
from dependencies import get_current_user
from models.usuario import Usuario

router = APIRouter(
    prefix="/postulaciones",
    tags=["Postulaciones"],
    dependencies=[Depends(get_current_user)]
)


@router.get("/", response_model=List[Postulacion], summary="Obtener todas las postulaciones")
def get_all_postulaciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtiene una lista de todas las postulaciones."""
    return PostulacionService.get_all_postulaciones(db, skip, limit)


@router.get("/{postulacion_id}", response_model=Postulacion, summary="Obtener una postulación por ID")
def get_postulacion(postulacion_id: int, db: Session = Depends(get_db)):
    """Obtiene una postulación específica por su ID."""
    return PostulacionService.get_postulacion_by_id(db, postulacion_id)


@router.post("/", response_model=Postulacion, status_code=status.HTTP_201_CREATED, summary="Crear una nueva postulación")
def create_postulacion(postulacion: PostulacionCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    """
    Crea una nueva postulación para una vacante.
    El `user_id` en el body debe coincidir con el del usuario autenticado.
    """
    # Opcional: Forzar que el user_id sea el del usuario autenticado
    postulacion.user_id = current_user.id
    return PostulacionService.create_postulacion(db, postulacion)


@router.put("/{postulacion_id}", response_model=Postulacion, summary="Actualizar el estado de una postulación")
def update_postulacion(postulacion_id: int, postulacion: PostulacionUpdate, db: Session = Depends(get_db)):
    """
    Actualiza el estado de una postulación (ej. "Enviada", "En revisión", "Aceptada").
    """
    return PostulacionService.update_postulacion(db, postulacion_id, postulacion)


@router.delete("/{postulacion_id}", status_code=status.HTTP_200_OK, summary="Eliminar una postulación")
def delete_postulacion(postulacion_id: int, db: Session = Depends(get_db)):
    """
    Elimina una postulación de la base de datos.
    """
    return PostulacionService.delete_postulacion(db, postulacion_id)