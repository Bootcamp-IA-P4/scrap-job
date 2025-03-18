import os
import pytest
import importlib
from db import creation
from psycopg2 import sql
from unittest.mock import patch, MagicMock

@patch("psycopg2.connect")
def test_create_database_success(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None

    with patch.dict(os.environ, {
        "DB_USER": "test_user",
        "DB_HOST": "test_host",
        "DB_PORT": "5432",
        "DB_NAME": "test_db",
        "DB_PASSWORD": "test_password",
    }):
        importlib.reload(creation)

        creation.create_database()
        mock_cursor.execute.assert_any_call("SELECT 1 FROM pg_database WHERE datname = %s;", ("test_db",))
        expected_query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier("test_db"))
        mock_cursor.execute.assert_any_call(expected_query)

@patch("psycopg2.connect")
def test_create_database_already_exists(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (1,)

    with patch.dict(os.environ, {
        "DB_USER": "test_user",
        "DB_HOST": "test_host",
        "DB_PORT": "5432",
        "DB_NAME": "test_db",
        "DB_PASSWORD": "test_password",
    }):
        importlib.reload(creation)

        creation.create_database()
        mock_cursor.execute.assert_any_call("SELECT 1 FROM pg_database WHERE datname = %s;", ("test_db",))
        expected_query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier("test_db"))
        with pytest.raises(AssertionError):
            mock_cursor.execute.assert_any_call(expected_query)