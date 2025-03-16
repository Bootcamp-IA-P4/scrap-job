import os
import psycopg2
import pandas as pd
from psycopg2 import sql
from dotenv import load_dotenv
from connection import connect_to_database

load_dotenv()

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_FILE = os.path.join(PROJECT_ROOT, "scrap_job", "companies.csv")

def create_table():
    try:
        conn = connect_to_database()
        if conn is None:
            return

        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                company_name TEXT NOT NULL,
                ebitda_source TEXT,
                cif_source TEXT,
                cif TEXT PRIMARY KEY,  -- CIF is the primary key
                ebitda_2023 NUMERIC
            );
        """)
        print("Table 'companies' created successfully.")

        conn.commit()

        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error creating table: {e}")

def insert_data():
    try:
        df = pd.read_csv(CSV_FILE)
        print("Columns in CSV file:", df.columns.tolist())

        conn = connect_to_database()
        if conn is None:
            return

        cur = conn.cursor()

        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO companies (company_name, ebitda_source, cif_source, cif, ebitda_2023)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (cif) DO NOTHING;  -- Skip if CIF already exists
            """, (row["Nombre de la empresa"], row["Fuente de la información EBITDA"],
                  row["Fuente de la información CIF"], row["CIF"], row["EBITDA 2023"]))

        conn.commit()
        print("Data inserted successfully.")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error inserting data: {e}")

if __name__ == "__main__":
    create_table()
    insert_data()