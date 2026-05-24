import os
import psycopg2
from psycopg2.extensions import connection as _connection, cursor as _cursor


def execute_sql_file(cur: _cursor, file_path: str) -> bool:
    """Reads a .sql file and executes its contents using the provided cursor.

    Args:
        cur (_cursor): An active psycopg2 cursor object.
        file_path (str): The absolute or relative path to the targeted SQL file.

    Returns:
        bool: True if the file executed successfully, False if the file path does not exist.
        
    Raises:
        Exception: Re-raises any database or syntax errors encountered during execution.
    """
    if not os.path.exists(file_path):
        print(f"Warning: File not found at {file_path}")
        return False
        
    print(f"Reading {os.path.basename(file_path)}...")
    with open(file_path, "r", encoding="utf-8") as f:
        sql_commands: str = f.read()
        
    try:
        cur.execute(sql_commands)
        print(f"Executed {os.path.basename(file_path)} successfully.")
        return True
    except Exception as e:
        print(f"Error executing {file_path}: {e}")
        raise


def main() -> None:
    """Orchestrates database connection, file parsing, and transactional rollbacks."""
    print("Connecting to database...")
    
    conn: _connection = psycopg2.connect(
        "dbname=postgres user=postgres password=postgres host=localhost"
    )
    
    try:
        with conn.cursor() as cur:
            seeding_scripts: list[str] = [
                "src/database/sql/queries/001_CREATE_INITIAL_SCHEMA.sql",
                "src/database/sql/queries/002_CREATE_USERS_TABLE.sql",
                "src/database/sql/queries/003_CREATE_VEHICLES_TABLE.sql",
                "src/database/sql/queries/004_CREATE_RENTALS_TABLE.sql"
                  ]

            for script in seeding_scripts:
                execute_sql_file(cur, script)
        conn.commit()
        print("Database successfully built and seeded via SQL scripts!")
        
    except Exception as e:
        conn.rollback()
        print(f"Transaction rolled back. Seeding failed: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()