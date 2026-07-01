# run.py
from app.app import app
from app.app import db_manager
from app.models.model import Base     # Import your declarative Base

from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.address import Address


__all__ = ["User", "Vehicle", "Address"]

if __name__ == "__main__":
    print("Initializing database tables...")
    # Use your clean manager method!
    db_manager.create_tables(Base)
    
    app.run(debug=True)