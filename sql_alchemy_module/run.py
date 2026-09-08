# run.py
from app.app import app, db_manager
from app.models.address import Address
from app.models.model import Base  # Import your declarative Base
from app.models.user import User
from app.models.vehicle import Vehicle

__all__ = ["Address", "User", "Vehicle"]

if __name__ == "__main__":
    print("Initializing database tables...")
    # Use your clean manager method!
    db_manager.create_tables(Base)

    app.run(debug=True)
