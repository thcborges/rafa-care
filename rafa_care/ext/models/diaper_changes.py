from rafa_care.ext.db import db


class DiaperChange(db.Model):
    __tablename__ = "diaper_changes"
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    has_pee = db.Column("has_pee", db.Boolean(), server_default=db.false())
    has_poop = db.Column("has_poop", db.Boolean(), server_default=db.false())
    changed_at = db.Column("changed_at", db.DateTime(), server_default=db.func.now())
    created_at = db.Column("created_at", db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(
        "updated_at",
        db.DateTime(),
        server_default=db.func.now(),
        onupdate=db.func.now(),
    )
