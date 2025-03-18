import os
import importlib
from db import config
from unittest.mock import patch

def test_db_config():
    # Mock environment variables
    with patch.dict(os.environ, {
        "POSTGRES_DB": "test_db",
        "POSTGRES_USER": "test_user",
        "POSTGRES_PASSWORD": "test_password",
        "POSTGRES_HOST": "test_host",
        "POSTGRES_PORT": "5432",
    }):
        # Reload the config module to reinitialize DB_CONFIG with the mocked environment variables
        importlib.reload(config)

        # Assert the values in DB_CONFIG
        assert config.DB_CONFIG["dbname"] == "test_db"
        assert config.DB_CONFIG["user"] == "test_user"
        assert config.DB_CONFIG["password"] == "test_password"
        assert config.DB_CONFIG["host"] == "test_host"
        assert config.DB_CONFIG["port"] == "5432"