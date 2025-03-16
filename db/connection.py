import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def connect_to_database():
    try:
        conn = psycopg2.connect(
            user=os.getenv("DB_USER"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            password=os.getenv("DB_PASSWORD")
        )
        print("Connection successful!")
        return conn
    except Exception as error:
        print(f"Error connecting to the database: {error}")
        return None

if __name__ == "__main__":
    if conn := connect_to_database():
        conn.close()