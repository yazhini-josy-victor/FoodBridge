
from datetime import datetime, timezone

from app import db


class Institution(db.Model):
    __tablename__ = "institutions"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    name = db.Column(db.String(180), nullable=False)
    institution_type = db.Column(db.String(40), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    maps_url = db.Column(db.String(1000), nullable=True)
    contact_person = db.Column(db.String(120), nullable=False)
    contact_number = db.Column(db.String(30), nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    user = db.relationship(
        "User",
        backref=db.backref("institution", uselist=False),
    )

    def __repr__(self):
        return f"<Institution id={self.id} name={self.name!r}>"
