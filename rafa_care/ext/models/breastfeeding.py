from rafa_care.ext.db import db
from rafa_care.ext.models import DiaperChange, MilkSource


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
    started_at = db.Column("started_at",
                           db.DateTime(),
                           nullable=True)
    finished_at = db.Column("finished_at",
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
