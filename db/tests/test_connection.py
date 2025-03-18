import psycopg2
from unittest.mock import patch
from db.connection import connect_to_database

@patch("psycopg2.connect")
def test_connect_to_database_success(mock_connect):
    # Mock a successful database connection
    mock_connect.return_value = "connection_object"

    # Mock environment variables
    with patch.dict("os.environ", {
        "DB_USER": "test_user",
        "DB_HOST": "test_host",
        "DB_PORT": "5432",
        "DB_NAME": "test_db",
        "DB_PASSWORD": "test_password",
    }):
        result = connect_to_database()
        assert result == "connection_object"

@patch("psycopg2.connect")
def test_connect_to_database_failure(mock_connect):
    # Mock a failed database connection
    mock_connect.side_effect = Exception("Connection failed")

    # Mock environment variables
    with patch.dict("os.environ", {
        "DB_USER": "test_user",
        "DB_HOST": "test_host",
        "DB_PORT": "5432",
        "DB_NAME": "test_db",
        "DB_PASSWORD": "test_password",
    }):
        result = connect_to_database()
        assert result is None