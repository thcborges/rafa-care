from rafa_care.ext.db import db
from rafa_care.ext.models import Medication


class MedicationDao:
    @staticmethod
    def get_by_id(id_) -> Medication:
        return db.session.query(Medication).filter(Medication.id == id_).first()

    @staticmethod
    def get_all():
        return (
            db.session.query(Medication).order_by(db.text("gave_at DESC")).all()
        )
