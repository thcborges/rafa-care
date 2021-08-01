from rafa_care.ext.db import db
from rafa_care.ext.models import Breastfeeding


class BreastfeedingDao:
    @staticmethod
    def get_by_id(id_) -> Breastfeeding:
        return db.session.query(Breastfeeding).filter(Breastfeeding.id == id_).first()

    @staticmethod
    def get_all():
        return (
            db.session.query(Breastfeeding).order_by(db.text("started_at DESC")).all()
        )
