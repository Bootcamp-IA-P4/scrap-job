import os
import psycopg2
from config import DB_CONFIG

def connect_to_database():
    try:
        conn = psycopg2.connect(
            user=DB_CONFIG["user"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            dbname=DB_CONFIG["dbname"],
            password=DB_CONFIG["password"],
        )
        print("Connection successful!")
        return conn
    except Exception as error:
        print(f"Error connecting to the database: {error}")
        return None

if __name__ == "__main__":
    if conn := connect_to_database():
        conn.close()
