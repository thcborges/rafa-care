from rafa_care.ext.db import db
from rafa_care.ext.models import MilkSource


class MilkSourceDao:
    @staticmethod
    def get_all() -> list[MilkSource]:
        return db.session.query(MilkSource).order_by(MilkSource.id).all()
