
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy.exc import IntegrityError

from app import create_app, db
from app.models import User, Donation


@pytest.fixture
def app():
    test_app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
        "WTF_CSRF_ENABLED": False,
    })

    with test_app.app_context():
        db.create_all()
        yield test_app
        db.session.remove()
        db.drop_all()


def test_donation_can_be_created(app):
    with app.app_context():
        donor = User(
            full_name="Test Donor",
            email="donor@example.com",
            role="donor",
        )
        donor.set_password("TestPassword123")
        db.session.add(donor)
        db.session.flush()

        now = datetime.now(timezone.utc)

        donation = Donation(
            donor_id=donor.id,
            food_name="Vegetable Rice",
            food_category="veg",
            food_type="cooked",
            quantity=10,
            quantity_unit="kg",
            estimated_servings=20,
            prepared_at=now,
            expires_at=now + timedelta(hours=8),
            pickup_deadline=now + timedelta(hours=6),
            pickup_address="Chennai",
            allow_partial=True,
            minimum_pickup_quantity=2,
        )

        db.session.add(donation)
        db.session.commit()

        saved_donation = db.session.get(Donation, donation.id)

        assert saved_donation is not None
        assert saved_donation.food_name == "Vegetable Rice"
        assert saved_donation.status == "AVAILABLE"
        assert saved_donation.allow_partial is True
        assert saved_donation.donor_id == donor.id


def test_donation_requires_valid_quantity(app):
    with app.app_context():
        donor = User(
            full_name="Test Donor",
            email="donor2@example.com",
            role="donor",
        )
        donor.set_password("TestPassword123")
        db.session.add(donor)
        db.session.flush()

        now = datetime.now(timezone.utc)

        donation = Donation(
            donor_id=donor.id,
            food_name="Rice",
            food_category="veg",
            food_type="cooked",
            quantity=0,
            quantity_unit="kg",
            estimated_servings=10,
            expires_at=now + timedelta(hours=8),
            pickup_deadline=now + timedelta(hours=6),
            pickup_address="Chennai",
            minimum_pickup_quantity=1,
        )

        db.session.add(donation)

        with pytest.raises(IntegrityError):
            db.session.commit()

        db.session.rollback()
