from sqlalchemy.orm import Session
from models.features import CVFeatures

class CVFeaturesDAO:

    @staticmethod
    def get_by_usuario(db: Session, usuario_id: int) -> CVFeatures | None:
        return db.query(CVFeatures).get(usuario_id)

    @staticmethod
    def upsert(db: Session, usuario_id: int, texto: str, skills: list, embedding: list[float]) -> CVFeatures:
        rec = db.query(CVFeatures).get(usuario_id)
        if rec:
            rec.texto = texto
            rec.skills = skills
            rec.embedding = embedding
        else:
            rec = CVFeatures(
                usuario_id=usuario_id,
                texto=texto,
                skills=skills,
                embedding=embedding
            )
            db.add(rec)
        db.commit(); db.refresh(rec)
        return rec