import psycopg2
from typing import TypedDict

class DBConfigOpts(TypedDict):
    dbname: str
    user: str
    password: str
    host: str
    port: str


def main():
    DB_CONFIG: DBConfigOpts = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432",
}
            
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            query = """
                SELECT id
                FROM lyfter_car_rental.vehicles
                WHERE vehicle_status = 'available';
            """
            with conn.cursor() as cur:
                cur.execute(query)
            if cur.rowcount == 0:
                print("DB ERROR. There are no vehicles available.")
                return
            print("DB OK. System operating normally.")
    except psycopg2.Error as pge:
        print(f"DB ERROR. {pge}")

if __name__ == "__main__":
    main()
