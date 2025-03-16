import os
import psycopg2
from psycopg2 import sql


DB_NAME = os.getenv("POSTGRES_DB")
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOST = os.getenv("POSTGRES_HOST")
PORT = os.getenv("POSTGRES_PORT")


def create_database():
    try:
        conn = psycopg2.connect(
            dbname="postgres", user=USER, password=PASSWORD, host=HOST, port=PORT
        )
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (DB_NAME,))
        if cur.fetchone():
            print(f"Database '{DB_NAME}' already exists.")
        else:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
            print(f"Database '{DB_NAME}' was created successfully.")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error connecting to database: {e}")


if __name__ == "__main__":
    create_database()
