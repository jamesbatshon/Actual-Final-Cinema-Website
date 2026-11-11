"""Initialize the cinema schema and securely create a staff account.

Usage (no demo data or seeding):
    python main.py init
    python main.py create-admin --admin-email manager@example.com
"""

import argparse
from getpass import getpass

from sqlalchemy import select

from app import create_app
from models import User, UserRole, db
from utils import EMAIL_PATTERN


def create_management_account(email, password):
    """Create one staff account; never promote an existing customer account."""
    email = email.strip().lower()
    if len(email) > 255 or not EMAIL_PATTERN.fullmatch(email):
        raise ValueError("Enter a valid staff email address.")
    if not 10 <= len(password) <= 128:
        raise ValueError("Staff password must have between 10 and 128 characters.")
    if db.session.scalar(select(User.id).where(User.email == email)) is not None:
        raise ValueError("An account already exists with that email.")

    user = User(email=email, role=UserRole.management_staff)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def main():
    parser = argparse.ArgumentParser(description="Screenlane MariaDB setup (no sample data)")
    parser.add_argument("command", nargs="?", choices=("init", "create-admin"), default="init")
    parser.add_argument("--admin-email", help="Email for the initial staff account")
    args = parser.parse_args()

    if args.command == "create-admin" and not args.admin_email:
        parser.error("create-admin requires --admin-email")

    app = create_app()
    with app.app_context():
        # Creates only tables that do not yet exist; does not add sample records.
        db.create_all()
        if args.command == "init":
            print("Database tables are ready. No sample data was added.")
            return

        password = getpass("Staff password (10-128 characters): ")
        confirmation = getpass("Confirm staff password: ")
        if password != confirmation:
            parser.error("The passwords do not match.")
        try:
            create_management_account(args.admin_email, password)
        except ValueError as exc:
            parser.error(str(exc))
        print(f"Management account created for {args.admin_email.strip().lower()}.")


if __name__ == "__main__":
    main()
