from rafa_care.ext.db import db
from rafa_care.ext.models import Medicine


class MedicineDao:
    @staticmethod
    def get_all() -> list[Medicine]:
        return db.session.query(Medicine).order_by(Medicine.id).all()
