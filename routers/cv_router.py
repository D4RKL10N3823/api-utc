"""
Router para endpoints de CV
"""
from fastapi import APIRouter, Depends, UploadFile, Form
from sqlalchemy.orm import Session
from database import get_db
from services.cv_service import CVService
from schemas.cv import CVResponse
from dependencies import get_current_user
from models.usuario import Usuario
from typing import List
from fastapi.responses import Response

router = APIRouter(
    prefix="/cv",
    tags=["CVs"]
)


@router.get("/", response_model=List[CVResponse])
def listar_cvs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtiene todos los CVs"""
    return CVService.get_all_cvs(db, skip, limit)


@router.get("/usuario/{usuario_id}", response_model=List[CVResponse])
def obtener_cvs_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtiene todos los CVs de un usuario específico"""
    return CVService.get_cvs_by_usuario(db, usuario_id)


@router.post("/", response_model=CVResponse, status_code=201)
def subir_cv(
    usuario_id: int = Form(...),
    archivo: UploadFile = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Sube un nuevo CV"""
    if archivo is None:
        raise HTTPException(status_code=400, detail="Debes enviar un archivo PDF")
    if archivo.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")
    return CVService.upload_cv(db, usuario_id, archivo)


@router.get("/descargar/{cv_id}")
def descargar_cv(
    cv_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Descarga un CV en formato PDF"""
    cv = CVService.get_cv_by_id(db, cv_id)
    return Response(
        content=cv.archivo,
        media_type=cv.tipo,
        headers={"Content-Disposition": f"attachment; filename={cv.nombre_archivo}"}
    )


@router.delete("/{cv_id}")
def eliminar_cv(
    cv_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Elimina un CV"""
    return CVService.delete_cv(db, cv_id)
