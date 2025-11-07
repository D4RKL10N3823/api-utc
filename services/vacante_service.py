"""
Service para orquestar operaciones de Vacante
"""
from sqlalchemy.orm import Session
from dao.vacante_dao import VacanteDAO
from schemas.vacante import VacanteCreate, VacanteUpdate
from models.vacante import Vacante
from typing import List, Optional
from fastapi import HTTPException, status
from services.vacante_features_service import VacanteFeaturesService
from dao.vacantes_features_dao import VacanteFeaturesDAO
from dao.cv_features_dao import CVFeaturesDAO
from utils import cv_matcher as cm

class VacanteService:
    """Service para la lógica de negocio de Vacante"""

    @staticmethod
    def get_all_vacantes(db: Session, skip: int = 0, limit: int = 100) -> List[Vacante]:
        """Obtiene todas las vacantes"""
        return VacanteDAO.get_all(db, skip, limit)

    @staticmethod
    def get_vacante_by_id(db: Session, vacante_id: int) -> Vacante:
        """Obtiene una vacante por ID"""
        vacante = VacanteDAO.get_by_id(db, vacante_id)
        if not vacante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vacante con ID {vacante_id} no encontrada"
            )
        return vacante

    @staticmethod
    def create_vacante(db: Session, vacante_data: VacanteCreate) -> Vacante:
        """Crea una nueva vacante"""
        try:
            vacante = VacanteDAO.create(
                db,
                nombre_empresa=vacante_data.nombre_empresa,
                datos_vacante=vacante_data.datos_vacante
            )

            VacanteFeaturesService.upsert_from_vacante(db, vacante)

            return vacante
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error al crear la vacante: {str(e)}"
            )

    @staticmethod
    def update_vacante(db: Session, vacante_id: int, vacante_data: VacanteUpdate) -> Vacante:
        """Actualiza una vacante existente"""
        # Verificar que existe
        VacanteService.get_vacante_by_id(db, vacante_id)
        
        # Actualizar solo los campos proporcionados
        vacante = VacanteDAO.update(
            db,
            vacante_id,
            nombre_empresa=vacante_data.nombre_empresa,
            datos_vacante=vacante_data.datos_vacante
        )
        
        if not vacante:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al actualizar la vacante"
            )
        
        VacanteFeaturesService.upsert_from_vacante(db, vacante)
        
        return vacante

    @staticmethod
    def delete_vacante(db: Session, vacante_id: int) -> dict:
        """Elimina una vacante"""
        # Verificar que existe
        VacanteService.get_vacante_by_id(db, vacante_id)
        
        success = VacanteDAO.delete(db, vacante_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al eliminar la vacante"
            )
        
        return {"message": "Vacante eliminada exitosamente"}

    @staticmethod
    def search_vacantes_by_empresa(db: Session, nombre_empresa: str) -> List[Vacante]:
        """Busca vacantes por nombre de empresa"""
        return VacanteDAO.search_by_empresa(db, nombre_empresa)
    
    @staticmethod
    def list_for_user_ranked(
        db: Session,
        usuario_id: int,
        topk: int = 100,
        alpha: float = 0.55, beta: float = 0.35, gamma: float = 0.10
    ) -> List[Vacante]:
        cvf = CVFeaturesDAO.get_by_usuario(db, usuario_id)
        if not cvf:
            # sin CV → regresa normal
            return VacanteDAO.get_all(db, 0, topk)

        vacs = VacanteDAO.get_all(db, 0, 10_000)
        if not vacs:
            return []

        feats = VacanteFeaturesDAO.get_by_ids(db, [v.id for v in vacs])
        fmap = {f.vacante_id: f for f in feats}

        docs_meta, embs, bm_corpus, kept = [], [], [], []
        for v in vacs:
            f = fmap.get(v.id)
            if not f:
                continue
            docs_meta.append({"id": str(v.id), "text": f.jd_text})
            embs.append(f.embedding)
            bm_corpus.append(cm.tokenize(f.jd_text))
            kept.append(v)

        if not docs_meta:
            return []

        bm25 = cm.BM25Okapi(bm_corpus)
        q_idx = cm.prepare_index([{"blocks":[{"title":"cv","text": cvf.texto}]}])

        order, final, cos, bm, ov = cm.hybrid_rank(
            q_idx, embs, bm25, docs_meta,
            alpha=alpha, beta=beta, gamma=gamma, topk=min(topk, len(docs_meta))
        )

        ranked = []
        for i in order:
            v = kept[i]
            # opcional: anexa info de match para el front
            setattr(v, "match_score", round(float(final[i]), 4))
            setattr(v, "match_terms", cm.pretty_overlap(ov, i))
            ranked.append(v)
        return ranked
