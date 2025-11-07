from sqlalchemy.orm import Session
from models.features import VacanteFeatures

class VacanteFeaturesDAO:

    @staticmethod
    def get_by_id(db: Session, vacante_id: int) -> VacanteFeatures | None:
        return db.query(VacanteFeatures).get(vacante_id)

    @staticmethod
    def get_by_ids(db: Session, ids: list[int]) -> list[VacanteFeatures]:
        return db.query(VacanteFeatures).filter(VacanteFeatures.vacante_id.in_(ids)).all()

    @staticmethod
    def upsert(db: Session, vacante_id: int, jd_text: str, jd_terms: list, embedding: list[float]) -> VacanteFeatures:
        rec = db.query(VacanteFeatures).get(vacante_id)
        if rec:
            rec.jd_text = jd_text
            rec.jd_terms = jd_terms
            rec.embedding = embedding
        else:
            rec = VacanteFeatures(
                vacante_id=vacante_id,
                jd_text=jd_text,
                jd_terms=jd_terms,
                embedding=embedding
            )
            db.add(rec)
        db.commit()
        db.refresh(rec)
        return rec