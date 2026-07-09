import random
import string
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.models import Base, User, Address, Vehicle

DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres?options=-csearch_path=sql_alchemy_module"

fake = Faker()

CAR_DATA = {
    "Toyota": ["Camry", "Corolla", "RAV4", "Tacoma", "Prius"],
    "Ford": ["F-150", "Mustang", "Explorer", "Escape", "Bronco"],
    "Honda": ["Civic", "Accord", "CR-V", "Pilot", "Odyssey"],
    "Chevrolet": ["Silverado", "Malibu", "Equinox", "Tahoe", "Corvette"],
    "Tesla": ["Model S", "Model 3", "Model X", "Model Y"],
}


def generate_random_vin() -> str:
    characters = string.ascii_uppercase + string.digits
    return "".join(random.choices(characters, k=17))

def assign_probabilistically[T](value: T) -> T | None:
    return None if random.random() < 0.10 else value


def seed_database():
    print("Connecting to the database...")
    engine = create_engine(DATABASE_URL)

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        print("Seeding database...")

        for i in range(20):
            user = User(
                full_name=fake.name(),
                email=fake.unique.email(),
                phone_number=fake.phone_number()[:16],
            )
            session.add(user)

            address = Address(
                physical_address=fake.address().replace("\n", ", "), user=user
            )
            session.add(address)

            if i < 4:
                num_vehicles = 0
            else:
                num_vehicles = random.randint(1, 3)

            for _ in range(num_vehicles):
                make = random.choice(list(CAR_DATA.keys()))
                model = random.choice(CAR_DATA[make])

                vehicle = Vehicle(
                    make=make,
                    model=model,
                    year=random.randint(1990, 2026),
                    vin=generate_random_vin(),
                    user=assign_probabilistically(user),
                )
                session.add(vehicle)

        try:
            session.commit()
            print("Successfully populated database")
        except Exception as e:
            session.rollback()
            print(f"An error occurred during commit: {e}")


if __name__ == "__main__":
    seed_database()
