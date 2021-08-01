from datetime import datetime, timezone

from rafa_care.ext.db import db
from rafa_care.ext.helpers.tz import convert_tz
from rafa_care.ext.models import Medicine

AMERICA_FORTALEZA_TIMEZONE = -3


class Medication(db.Model):
    __tablename__ = "medications"
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    medicine_id = db.Column(
        "medicine_id",
        db.Integer,
        db.ForeignKey("medicines.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )
    __gave_at = db.Column("gave_at", db.DateTime(), nullable=True)
    note = db.Column("note", db.UnicodeText(), nullable=True)
    created_at = db.Column("created_at", db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(
        "updated_at",
        db.DateTime(),
        server_default=db.func.now(),
        onupdate=db.func.now(),
    )

    medicine = db.relationship(Medicine, backref="medicines")

    @property
    def gave_at(self):
        return convert_tz(self.__gave_at, AMERICA_FORTALEZA_TIMEZONE)

    @property
    def input_gave_at(self) -> str:
        if not self.__gave_at:
            return ""
        return self.gave_at.strftime("%Y-%m-%dT%H:%M")

    @property
    def formatted_gave_at(self) -> str:
        if not self.__gave_at:
            return ""
        return self.gave_at.strftime("%d/%m/%Y %H:%M")

    @gave_at.setter
    def gave_at(self, value):
        if isinstance(value, str):
            self.__gave_at = datetime.fromisoformat(
                f"{value}{AMERICA_FORTALEZA_TIMEZONE:+03d}:00"
            ).astimezone(timezone.utc)
        elif isinstance(value, datetime):
            self.__gave_at = value.astimezone(timezone.utc)

    @classmethod
    def give(cls, medicine_id):
        gave_at = datetime.utcnow()
        return cls(gave_at=gave_at, medicine_id=medicine_id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, medicine_id, gave_at, note):
        self.medicine_id = medicine_id
        self.gave_at = gave_at
        self.note = note
        self.save()
