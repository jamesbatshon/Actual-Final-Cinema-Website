"""Database setup without demo data and secure administrator provisioning."""

from sqlalchemy import func, select

from app import create_app
from main import create_management_account
from models import Movie, TicketPrice, User, UserRole, db


def test_empty_schema_does_not_require_demo_data(tmp_path):
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "unit-tests-only",
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path / 'empty.db'}",
    })
    with app.app_context():
        db.create_all()
        assert db.session.scalar(select(func.count()).select_from(Movie)) == 0
        assert db.session.scalar(select(func.count()).select_from(TicketPrice)) == 0
        assert db.session.scalar(select(func.count()).select_from(User)) == 0
        # Re-initialising must not overwrite data or add example records.
        db.create_all()
        assert db.session.scalar(select(func.count()).select_from(User)) == 0


def test_create_management_account_without_seeding(app):
    with app.app_context():
        user = create_management_account(" NEW-MANAGER@example.com ", "long-unique-password-123")
        assert user.email == "new-manager@example.com"
        assert user.role == UserRole.management_staff
        assert user.password != "long-unique-password-123"
        assert user.check_password("long-unique-password-123")
