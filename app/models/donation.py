
from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, Numeric
from app import db


class Donation(db.Model):
    __tablename__ = "donations"

    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_donation_quantity_positive"),
        CheckConstraint(
            "estimated_servings > 0",
            name="ck_donation_servings_positive",
        ),
        CheckConstraint(
            "minimum_pickup_quantity > 0",
            name="ck_donation_minimum_quantity_positive",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    # Donor who created this donation
    donor_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    # Food details
    food_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    food_category = db.Column(db.String(20), nullable=False)
    food_type = db.Column(db.String(40), nullable=False)

    # Quantity details
    quantity = db.Column(Numeric(10, 2), nullable=False)
    quantity_unit = db.Column(db.String(30), nullable=False)
    estimated_servings = db.Column(db.Integer, nullable=False)

    # Food safety details
    prepared_at = db.Column(db.DateTime(timezone=True), nullable=True)
    expires_at = db.Column(db.DateTime(timezone=True), nullable=False)
    pickup_deadline = db.Column(db.DateTime(timezone=True), nullable=False)

    storage_instructions = db.Column(db.Text, nullable=True)
    allergens = db.Column(db.JSON, nullable=False, default=list)
    dietary_information = db.Column(db.Text, nullable=True)

    # Partial allocation settings
    allow_partial = db.Column(db.Boolean, nullable=False, default=False)
    minimum_pickup_quantity = db.Column(
        Numeric(10, 2),
        nullable=False,
        default=1,
    )

    # Collection details
    pickup_address = db.Column(db.String(300), nullable=False)
    maps_url = db.Column(db.String(1000), nullable=True)
    delivery_available = db.Column(db.Boolean, nullable=False, default=False)

    # Donation lifecycle
    status = db.Column(
        db.String(30),
        nullable=False,
        default="AVAILABLE",
        index=True,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    donor = db.relationship(
        "User",
        backref=db.backref("donations", lazy=True),
    )

    def __repr__(self):
        return (
            f"<Donation id={self.id} "
            f"food_name={self.food_name!r} status={self.status!r}>"
        )
