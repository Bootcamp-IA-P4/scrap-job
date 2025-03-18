import os
import pandas as pd
from unittest.mock import patch, MagicMock
from db.load_companies import create_table, insert_data

@patch("db.load_companies.connect_to_database")
def test_create_table_success(mock_connect):
    # Mock the database connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Mock environment variables if needed
    with patch.dict(os.environ, {
        "DB_USER": "test_user",
        "DB_HOST": "test_host",
        "DB_PORT": "5432",
        "DB_NAME": "test_db",
        "DB_PASSWORD": "test_password",
    }):
        create_table()
        # Verify that the CREATE TABLE query was executed with the correct SQL
        mock_cursor.execute.assert_any_call("""
            CREATE TABLE IF NOT EXISTS companies (
                company_name TEXT NOT NULL,
                ebitda_source TEXT,
                cif_source TEXT,
                cif TEXT PRIMARY KEY,  -- CIF is the primary key
                ebitda_2023 NUMERIC
            );
        """)

@patch("db.load_companies.connect_to_database")
@patch("pandas.read_csv")
def test_insert_data_success(mock_read_csv, mock_connect):
    # Mock the database connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Mock the CSV file
    mock_df = pd.DataFrame({
        "Nombre de la empresa": ["Company A"],
        "Fuente de la información EBITDA": ["http://example.com"],
        "Fuente de la información CIF": ["http://example.com"],
        "CIF": ["A12345678"],
        "EBITDA 2023": [1000000],
    })
    mock_read_csv.return_value = mock_df

    # Mock the CSV file path
    with patch("db.load_companies.CSV_FILE", "dummy_path.csv"):
        insert_data()

        # Verify that the CSV file was read
        mock_read_csv.assert_called_once_with("dummy_path.csv")

        # Expected SQL query (normalized)
        expected_query = """INSERT INTO companies (company_name, ebitda_source, cif_source, cif, ebitda_2023)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (cif) DO NOTHING;  -- Skip if CIF already exists
        """
        expected_query = " ".join(expected_query.split())  # Normalize query format

        # Expected parameters
        expected_params = ("Company A", "http://example.com", "http://example.com", "A12345678", 1000000)

        # Extract actual query and parameters from mock
        actual_query, actual_params = mock_cursor.execute.call_args[0]  # Get both query and parameters

        # Normalize actual query
        actual_query = " ".join(actual_query.split())

        # Assert queries match
        assert expected_query == actual_query, f"Expected: {expected_query}, but got: {actual_query}"

        # Assert parameters match
        assert expected_params == actual_params, f"Expected params: {expected_params}, but got: {actual_params}"

        # Verify that the connection was committed and closed
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

@patch("db.load_companies.connect_to_database")
@patch("pandas.read_csv")
def test_insert_data_error(mock_read_csv, mock_connect):
    # Mock the database connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Simulate a missing CSV file
    mock_read_csv.side_effect = FileNotFoundError("CSV file not found")

    # Mock the CSV file path
    with patch("db.load_companies.CSV_FILE", "dummy_path.csv"):
        insert_data()
        # Verify that the error was handled gracefully
        mock_cursor.execute.assert_not_called()