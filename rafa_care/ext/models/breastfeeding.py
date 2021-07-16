from datetime import datetime, timezone

from rafa_care.ext.db import db
from rafa_care.ext.helpers.tz import convert_tz
from rafa_care.ext.models import DiaperChange, MilkSource

AMERICA_FORTALEZA_TIMEZONE = -3


class Breastfeeding(db.Model):
    __tablename__ = "breastfeeding"
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    milk_source_id = db.Column("milk_source_id",
                               db.Integer,
                               db.ForeignKey("milk_sources.id",
                                             onupdate="CASCADE",
                                             ondelete="SET NULL"),
                               nullable=True)
    diaper_change_id = db.Column("diaper_change_id",
                                 db.Integer,
                                 db.ForeignKey("diaper_changes.id",
                                               onupdate="CASCADE",
                                               ondelete="SET NULL"))
    __started_at = db.Column("started_at",
                           db.DateTime(),
                           nullable=True)
    __finished_at = db.Column("finished_at",
                            db.DateTime(),
                            nullable=True)
    note = db.Column("note", db.UnicodeText(), nullable=True)
    created_at = db.Column("created_at",
                           db.DateTime(),
                           server_default=db.func.now())
    updated_at = db.Column("updated_at",
                           db.DateTime(),
                           server_default=db.func.now(),
                           onupdate=db.func.now())

    milk_source = db.relationship(MilkSource, backref="breastfeeding")
    diaper_change = db.relationship(DiaperChange, backref="breastfeeding")

    @property
    def started_at(self):
        return convert_tz(self.__started_at, AMERICA_FORTALEZA_TIMEZONE)

    @property
    def input_started_at(self) -> str:
        if not self.__started_at:
            return ""
        return self.started_at.strftime('%Y-%m-%dT%H:%M')

    @property
    def formatted_started_at(self) -> str:
        if not self.__started_at:
            return ""
        return self.started_at.strftime('%d/%m/%Y %H:%M')

    @started_at.setter
    def started_at(self, value):
        if isinstance(value, str):
            self.__started_at = (
                datetime.fromisoformat(
                    f"{value}{AMERICA_FORTALEZA_TIMEZONE:+03d}:00"
                ).astimezone(timezone.utc)
            )
        elif isinstance(value, datetime):
            self.__started_at = value.astimezone(timezone.utc)

    @property
    def finished_at(self):
        return convert_tz(self.__finished_at, AMERICA_FORTALEZA_TIMEZONE)

    @property
    def input_finished_at(self) -> str:
        if not self.__finished_at:
            return ""
        return self.finished_at.strftime('%Y-%m-%dT%H:%M')

    @property
    def formatted_finished_at(self) -> str:
        if not self.__finished_at:
            return ""
        return self.finished_at.strftime('%d/%m/%Y %H:%M')

    @finished_at.setter
    def finished_at(self, value):
        if isinstance(value, str):
            self.__finished_at = (
                datetime.fromisoformat(
                    f"{value}{AMERICA_FORTALEZA_TIMEZONE:+03d}:00"
                ).astimezone(timezone.utc)
            )
        elif isinstance(value, datetime):
            self.__finished_at = value.astimezone(timezone.utc)

    @property
    def duration(self) -> str:
        if not self.__finished_at or not self.__started_at:
            return ""
        delta = self.__finished_at - self.__started_at
        total_seconds = int(delta.total_seconds())
        minutes = total_seconds % 3600 // 60
        hours = total_seconds // 3600
        return f"{hours:02d}:{minutes:02d}"

    @classmethod
    def start(cls):
        started_at = datetime.utcnow()
        return cls(started_at=started_at)

    def finish(self, milk_source_id, started_at, note):
        self.milk_source_id = milk_source_id
        self.started_at = started_at
        self.note = note
        self.__finished_at = datetime.utcnow()
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, milk_source_id, started_at, finished_at, note):
        self.milk_source_id = milk_source_id
        self.started_at = started_at
        self.finished_at = finished_at
        self.note = note
        self.save()
