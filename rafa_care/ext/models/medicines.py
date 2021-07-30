from rafa_care.ext.db import db


class Medicine(db.Model):
    __tablename__ = "medicines"
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column("name", db.Unicode(50), nullable=False, unique=True)
    dosage = db.Column("dosage", db.Unicode(30))
    created_at = db.Column("created_at", db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(
        "updated_at",
        db.DateTime(),
        server_default=db.func.now(),
        onupdate=db.func.now(),
    )

    def __str__(self):
        return self.name
