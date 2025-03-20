from db.connection import connect_to_database

def get_companies():
    conn = connect_to_database()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM companies")
                companies = cursor.fetchall()
                return companies
        except Exception as error:
            print(f"Error fetching companies: {error}")
        finally:
            conn.close()
    return []

def get_company_by_cif(cif: str):
    conn = connect_to_database()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM companies WHERE CIF = %s", (cif,))
                company = cursor.fetchone()
                return company
        except Exception as error:
            print(f"Error fetching company: {error}")
        finally:
            conn.close()
    return None

def delete_company_by_cif(cif: str):
    conn = connect_to_database()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM companies WHERE CIF = %s", (cif,))
                conn.commit()
                return True
        except Exception as error:
            print(f"Error deleting company: {error}")
            conn.rollback()
        finally:
            conn.close()
    return False

def update_company_by_cif(cif: str, company_name: str, ebitda_source: str, cif_source: str, ebitda_2023: float):
    conn = connect_to_database()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE companies
                    SET company_name = %s,
                        ebitda_source = %s,
                        cif_source = %s,
                        ebitda_2023 = %s
                    WHERE CIF = %s
                    """,
                    (company_name, ebitda_source, cif_source, ebitda_2023, cif)
                )
                conn.commit()
                return True
        except Exception as error:
            print(f"Error updating company: {error}")
            conn.rollback()
        finally:
            conn.close()
    return False

def create_company(company_name: str, ebitda_source: str | None, cif_source: str | None, cif: str, ebitda_2023: float | None):
    conn = connect_to_database()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO companies (company_name, ebitda_source, cif_source, cif, ebitda_2023)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (company_name, ebitda_source, cif_source, cif, ebitda_2023)
                )
                conn.commit()
                print("Company created successfully!")
                return True
        except Exception as error:
            print(f"Error creating company: {error}")
            conn.rollback()
        finally:
            conn.close()
    return False