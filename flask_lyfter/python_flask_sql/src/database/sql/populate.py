import psycopg2
import random

from datetime import date
from faker import Faker
from typing import TypedDict
from typing import Tuple, List
from psycopg2.extensions import connection


fake = Faker()


class DBConfigOpts(TypedDict):
    dbname: str
    user: str
    password: str
    host: str
    port: str


DB_CONFIG: DBConfigOpts = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432",
}


def _generate_users_tuple(
    quantity: int = 1,
) -> List[Tuple[str, str, str, str, date, str]]:

    user_tuples: List[Tuple[str, str, str, str, date, str]] = []
    for _ in range(quantity):
        user_tuples.append(
            (
                fake.email(),
                fake.user_name(),
                fake.password(),
                fake.name(),
                fake.date_of_birth(minimum_age=15, maximum_age=99),
                random.choices(["active", "closed", "delinquent"], [0.9, 0.05, 0.05])[
                    0
                ],
            )
        )
    return user_tuples


def _create_single_user(conn: connection) -> int:
    user_data = _generate_users_tuple()[0]

    query = """
        INSERT INTO lyfter_car_rental.users 
        (email, username, password, full_name, birthdate, account_status) 
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
    """

    with conn.cursor() as cur:
        cur.execute(query, user_data)
        result = cur.fetchone()

        if result is None:
            raise RuntimeError("Unable to create user in database")
        return result[0]


def populate_users_table(conn: connection, quantity: int = 1):
    try:
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO lyfter_car_rental.users (email, username, password, full_name, birthdate, account_status) VALUES (%s, %s, %s, %s, %s, %s)",
                _generate_users_tuple(quantity),
            )
    except Exception as e:
        print(f"Error while populating users table: {e}")


def _generate_vehicles_tuple(quantity: int = 1) -> List[Tuple[str, str, int, str]]:
    VEHICLE_DATA = {
        "Toyota": ["Camry", "Corolla", "RAV4", "Tacoma", "Prius", "Highlander"],
        "Ford": ["F-150", "Mustang", "Explorer", "Escape", "Bronco", "Maverick"],
        "Honda": ["Civic", "Accord", "CR-V", "Pilot", "Odyssey", "Ridgeline"],
        "Chevrolet": ["Silverado", "Equinox", "Malibu", "Tahoe", "Colorado", "Bolt EV"],
        "Hyundai": ["Elantra", "Sonata", "Tucson", "Santa Fe", "Palisade", "Ioniq 5"],
        "Subaru": ["Outback", "Forester", "Impreza", "Crosstrek", "Ascent"],
        "Tesla": ["Model 3", "Model Y", "Model S", "Model X", "Cybertruck"],
        "BMW": ["3 Series", "5 Series", "X3", "X5", "i4"],
        "Mercedes-Benz": ["C-Class", "E-Class", "GLC", "GLE", "EQE"],
        "Jeep": ["Wrangler", "Grand Cherokee", "Cherokee", "Compass", "Gladiator"],
    }

    vehicle_tuples: List[Tuple[str, str, int, str]] = []
    for _ in range(quantity):
        make = random.choices(list(VEHICLE_DATA.keys()))[0]
        model = random.choice(VEHICLE_DATA[make])
        model_year = random.randint(2005, 2026)
        vehicle_status = random.choices(
            [
                "rented",
                "in_maintenance",
                "available",
                "unavailable",
                "reserved",
            ],
            [0.2, 0.05, 0.7, 0.04, 0.01],
        )[0]

        vehicle_tuples.append((make, model, model_year, vehicle_status))
    return vehicle_tuples


def _create_single_vehicle(conn: connection) -> int:
    vehicle_data = _generate_vehicles_tuple()[0]
    query = """
        INSERT INTO lyfter_car_rental.vehicles 
        (make, model, model_year, vehicle_status) 
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """
    with conn.cursor() as cur:
        cur.execute(query, vehicle_data)
        result = cur.fetchone()

        if result is None:
            raise RuntimeError("Unable to create vehicle in database")
        return result[0]


def populate_vehicles_table(conn: connection, quantity: int = 1):
    with conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO lyfter_car_rental.vehicles (make, model, model_year, vehicle_status) VALUES (%s, %s, %s, %s)",
            _generate_vehicles_tuple(quantity),
        )


def populate_rentals_table(conn: connection, quantity: int = 1):
    with conn.cursor() as cur:
        for _ in range(quantity):
            users_id = _create_single_user(conn)
            vehicles_id = _create_single_vehicle(conn)

            rental_date = fake.date_between(start_date="-1y", end_date="today")
            rental_status = random.choice(
                [
                    "pending",
                    "confirmed",
                    "ready_for_pickup",
                    "active",
                    "overdue",
                    "completed",
                    "cancelled",
                    "no_show",
                ]
            )

            rental_query = """
                        INSERT INTO lyfter_car_rental.rentals 
                        (users_id, vehicles_id, rental_date, rental_status) 
                        VALUES (%s, %s, %s, %s);
                    """

            cur.execute(
                rental_query, (users_id, vehicles_id, rental_date, rental_status)
            )


if __name__ == "__main__":
    try:
        seed_parameters = {
            "user_quantity": 10,
            "vehicle_quantity": 5,
            "rentals_quantity": 10,
        }

        with psycopg2.connect(**DB_CONFIG) as conn:
            populate_users_table(conn, seed_parameters["user_quantity"])
            populate_vehicles_table(conn, seed_parameters["vehicle_quantity"])
            populate_rentals_table(conn, seed_parameters["rentals_quantity"])

        print("Successfully added:")
        print(f"  {seed_parameters['user_quantity']} users")
        print(f"  {seed_parameters['vehicle_quantity']} vehicles")
        print(f"  {seed_parameters['rentals_quantity']} rentals")

    except Exception as e:
        print(f"Populate script failed with error: {e}")
