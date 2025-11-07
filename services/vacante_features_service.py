"""
Service para la extracción y persistencia de features de vacantes.
"""
from sqlalchemy.orm import Session
from utils import cv_matcher as cm
from dao.vacantes_features_dao import VacanteFeaturesDAO

class VacanteFeaturesService:
    """Service para generar y actualizar los features de una vacante (texto, términos, embedding)."""

    @staticmethod
    def _vacante_text_from_json(datos: dict) -> str:
        """Convierte el JSON de una vacante en un texto unificado para embeddings."""
        campos = ["titulo", "descripcion", "requisitos", "responsabilidades", "ubicacion", "tipo", "salario"]
        parts = []
        for k in campos:
            v = (datos or {}).get(k)
            if isinstance(v, list):
                parts.append(" ".join(map(str, v)))
            elif v:
                parts.append(str(v))
        return "\n".join(parts)

    @staticmethod
    def build_features(datos: dict) -> tuple[str, list, list[float]]:
        """Genera jd_text, jd_terms y embedding a partir de los datos de la vacante."""
        jd_text = VacanteFeaturesService._vacante_text_from_json(datos)
        jd_terms = cm.dedup_fuzzy(
            list(set(cm.keyphrases_spacy(jd_text) + cm.keyphrases_rake(jd_text)))
        )
        emb = cm.EMB.encode([jd_text])[0].tolist()
        return jd_text, jd_terms, emb

    @staticmethod
    def upsert_from_vacante(db: Session, vacante):
        """
        Recibe una instancia de Vacante (con datos_vacante)
        y crea/actualiza su registro en vacante_features.
        """
        datos = vacante.datos_vacante or {}
        jd_text, jd_terms, emb = VacanteFeaturesService.build_features(datos)
        return VacanteFeaturesDAO.upsert(db, vacante.id, jd_text, jd_terms, emb)
