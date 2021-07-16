from rafa_care.ext.db import db


class MilkSource(db.Model):
    __tablename__ = "milk_sources"
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    description = db.Column("description",
                            db.Unicode(50),
                            nullable=False,
                            unique=True)
    created_at = db.Column("created_at",
                           db.DateTime(),
                           server_default=db.func.now())
    updated_at = db.Column("updated_at",
                           db.DateTime(),
                           server_default=db.func.now(),
                           onupdate=db.func.now())

    def __str__(self):
        return self.description
