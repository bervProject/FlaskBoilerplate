import os
import pytest
from web import create_app


@pytest.fixture(scope="session")
def app():
    app = create_app({
        'TESTING': True,
        'PONY': {
            'provider': 'postgres',
            'user': os.environ.get('PG_USER', 'postgres'),
            'password': os.environ.get('PG_PASSWORD', 'devpassword'),
            'host': os.environ.get('PG_HOST', 'localhost'),
            'database': os.environ.get('PG_DB_NAME', 'bookdb')
        }
    })
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
