import os
from datetime import datetime
import psycopg2
from psycopg2 import sql 
from psycopg2.extensions import connection

from typing import TypedDict

class DBConfigOpts(TypedDict):
    dbname: str
    user: str
    password: str
    host: str
    port: str


def export_table_to_csv(conn: connection, table_name: str, output_dir: str):
    current_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    csv_file_path = os.path.join(output_dir, f"{table_name}_{current_time}.csv")
    schema: str = "lyfter_car_rental" 

    query = sql.SQL("COPY {} TO STDOUT WITH CSV HEADER").format(sql.Identifier(schema, table_name))

    with open(csv_file_path, 'w', encoding='utf-8') as f:
        with conn.cursor() as cur:
            query_string = query.as_string(conn)
            cur.copy_expert(query_string, f)
            

def get_tables_names(conn: connection) -> list[str]:
    """Queries the database and returns a list of all table names for lyfter_car_rental schema."""
    schema: str = "lyfter_car_rental"

    query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = %s;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (schema,))
            records = cur.fetchall()
            tables = [row[0] for row in records]
        return tables
    except Exception:
        raise

def main():
    DB_CONFIG: DBConfigOpts = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432",
}
            
    BACKUP_DIR = "./backup_dir"
    os.makedirs(BACKUP_DIR, exist_ok=True)

    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            # get all the table names:
            table_list = get_tables_names(conn)

            for table in table_list:
                export_table_to_csv(conn, table, BACKUP_DIR)
                
            print(f"{ ', '.join(table_list)} successfully backup at {BACKUP_DIR}")
    except Exception as e:
        print(e)

   
if __name__ == "__main__":
    main()

